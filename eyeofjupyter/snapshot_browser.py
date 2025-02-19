import json
import os
import subprocess
import webbrowser
from dataclasses import dataclass
from datetime import datetime
from importlib.resources import files
from typing import Optional

import waitress
from flask import Flask, request
from nbconvert import HTMLExporter

from eyeofjupyter import config
from eyeofjupyter.errors import NoSnapShotFile
from eyeofjupyter.fs_format import is_snapshot_folder
from eyeofjupyter.key_value_cache import KeyValueCache


def list_snapshotted_files(path):
    if not os.path.isdir(path):
        return []
    if len(sub_dirs := os.listdir(path)) == 0:
        return []
    if is_snapshot_folder(f"{path}{sub_dirs[0]}"):
        return [path]
    return [i for e in os.listdir(path) for i in list_snapshotted_files(f"{path}{e}/")]


@dataclass
class FileVersionDetails:
    file_name: str
    snapshot_datetime: datetime
    comment: Optional[str]


def get_file_versions_details(path):
    def get_file_version_details(file):
        metadata_file = os.path.join(path, file, config.METADATA_FILE)
        with open(metadata_file) as f:
            metadata = json.load(f)
            return FileVersionDetails(
                file_name=file,
                snapshot_datetime=datetime.fromisoformat(metadata["snapshot datetime"]),
                comment=metadata["comment"] if "comment" in metadata else None,
            )

    return [get_file_version_details(e) for e in os.listdir(path)]


def _create_ipynb_to_html_exporter():
    jinja_templates_folder = str(files("eyeofjupyter").joinpath("nbconvert_templates"))
    ipynb_to_html_exporter = HTMLExporter(
        template_name="default", extra_template_basedirs=jinja_templates_folder
    )
    ipynb_to_html_exporter.exclude_input_prompt = True
    ipynb_to_html_exporter.sanitize_html
    return ipynb_to_html_exporter


def get_static_folder():
    return str(files("eyeofjupyter").joinpath("static"))


def start_browser(snapshots_root_dir):
    app = Flask(__name__)

    ipynb_to_html_exporter = _create_ipynb_to_html_exporter()
    snapshot_html_cache = KeyValueCache()
    app.static_folder = get_static_folder()

    def get_html_preview(snapshot):
        if snapshot in snapshot_html_cache:
            return snapshot_html_cache[snapshot]

        if os.path.exists(
            snapshot_file
            := f"{snapshots_root_dir}{snapshot}/{config.SNAPSHOT_FILE_NAME}"
        ):
            (body, _metadata) = ipynb_to_html_exporter.from_filename(snapshot_file)
        elif os.path.exists(
            snapshot_file := f"{snapshots_root_dir}{snapshot}/report.html"
        ):
            with open(snapshot_file) as f:
                body = f.read()
        else:
            raise NoSnapShotFile(f"{snapshots_root_dir}{snapshot}")

        snapshot_html_cache[snapshot] = body
        return body

    @app.route("/list/files")
    def list_files():
        files = list_snapshotted_files(snapshots_root_dir)
        files = [os.path.relpath(e, snapshots_root_dir) for e in files]
        return sorted(files)

    @app.route("/list/versions/<path:file>")
    def list_versions(file):
        versions = get_file_versions_details(os.path.join(snapshots_root_dir, file))
        versions.sort(key=lambda e: e.snapshot_datetime, reverse=True)
        return versions

    @app.route("/snapshot/<path:snapshot>")
    def get_snapshot(snapshot):
        return get_html_preview(snapshot)

    @app.post("/diff")
    def diff():
        data = request.json
        file_a = os.path.join(
            snapshots_root_dir, data["baseFile"], data["first"], "snapshot.ipynb"
        )
        file_b = os.path.join(
            snapshots_root_dir, data["baseFile"], data["second"], "snapshot.ipynb"
        )
        cp = subprocess.run(["nbdiff-web", file_a, file_b], check=True)
        return str(cp.returncode == 0)

    @app.route("/")
    @app.route("/<path:file>")
    def static_file_server(file=None):
        if file is None:
            file = "index.html"
        return app.send_static_file(file)

    webbrowser.open_new_tab(f"http://localhost:{config.PORT}")

    if config.DEBUG:
        app.run(debug=True, port=config.PORT)
    else:
        waitress.serve(app, port=config.PORT)
