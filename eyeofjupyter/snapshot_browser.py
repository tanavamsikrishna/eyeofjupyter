from importlib.resources import files
import os
import webbrowser
from flask import Flask
from jinja2 import DictLoader
from nbconvert import HTMLExporter
import waitress
from eyeofjupyter import config
from eyeofjupyter.errors import NoSnapShotFile

from eyeofjupyter.fs_format import is_snapshot_folder
from eyeofjupyter.key_value_cache import KeyValueCache


def get_snapshots(path):
    if not os.path.isdir(path):
        return []
    if is_snapshot_folder(path):
        return [path]
    return [i for e in os.listdir(path) for i in get_snapshots(f"{path}{e}/")]


def _create_ipynb_to_html_exporter():
    jinja_templates_folder = str(
        files("eyeofjupyter").joinpath("templates").joinpath("nbconvert")
    )
    jinja_templates_folder = f"{jinja_templates_folder}/"

    templates = {}
    for file in os.listdir(jinja_templates_folder):
        with open(f"{jinja_templates_folder}{file}") as f:
            templates[file] = f.read()
    dl = DictLoader(templates)

    ipynb_to_html_exporter = HTMLExporter(
        extra_loaders=[dl], template_file="report_template.html.j2"
    )
    ipynb_to_html_exporter.exclude_input_prompt = True
    return ipynb_to_html_exporter


def start_browser(root):
    app = Flask(__name__)

    ipynb_to_html_exporter = _create_ipynb_to_html_exporter()
    snapshot_html_cache = KeyValueCache()

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

    @app.route("/snapshots")
    def list_snapshots():
        snapshots = get_snapshots(root)
        snapshots = [os.path.relpath(e, root) for e in snapshots]
        return snapshots

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
