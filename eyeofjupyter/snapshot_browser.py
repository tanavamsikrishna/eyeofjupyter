from importlib.resources import files
import os
import webbrowser
from flask import Flask
from nbconvert import HTMLExporter
import waitress
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


def list_file_versions(path):
    return os.listdir(path)


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


def start_browser(root):
    app = Flask(__name__)

    ipynb_to_html_exporter = _create_ipynb_to_html_exporter()
    snapshot_html_cache = KeyValueCache()
    app.static_folder = get_static_folder()

    def get_html_preview(snapshot):
        if snapshot in snapshot_html_cache:
            return snapshot_html_cache[snapshot]

        if os.path.exists(snapshot_file := f"{root}{snapshot}/snapshot.ipynb"):
            (body, _metadata) = ipynb_to_html_exporter.from_filename(snapshot_file)
        elif os.path.exists(snapshot_file := f"{root}{snapshot}/report.html"):
            with open(snapshot_file) as f:
                body = f.read()
        else:
            raise NoSnapShotFile(f"{root}{snapshot}")

        snapshot_html_cache[snapshot] = body
        return body

    @app.route("/list/files")
    def list_snapshots():
        snapshots = list_snapshotted_files(root)
        snapshots = [os.path.relpath(e, root) for e in snapshots]
        return snapshots

    @app.route("/list/versions/<path:file>")
    def list_versions(file):
        versions = list_file_versions(f"{root}{file}")
        return versions

    @app.route("/snapshot/<path:snapshot>")
    def get_snapshot(snapshot):
        return get_html_preview(snapshot)

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
