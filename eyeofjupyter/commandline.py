from datetime import datetime
import json
import os
import click
from nbconvert import HTMLExporter

from eyeofjupyter.fs_format import (
    get_new_snapshot_loc,
    get_project_root,
    get_snapshot_metadatafile,
    get_snapshot_report_file,
)
from eyeofjupyter.snapshot_browser import start_browser


@click.group()
def cli():
    pass


@cli.command()
@click.argument(
    "ipynbfile", type=click.Path(exists=True, readable=True, resolve_path=True)
)
def take_snapshot(ipynbfile):
    new_snapshot_version_loc = get_new_snapshot_loc(ipynbfile, get_project_root())
    os.makedirs(new_snapshot_version_loc)

    he = HTMLExporter()
    (body, _resources) = he.from_file(ipynbfile)
    metadata = {"snapshot datetime": datetime.now().isoformat()}
    with open(get_snapshot_report_file(new_snapshot_version_loc), "w+") as f:
        f.write(body)
    with open(get_snapshot_metadatafile(new_snapshot_version_loc), "w+") as f:
        json.dump(metadata, f)


@cli.command()
@click.option("--path", type=click.Path(resolve_path=True))
def browse(path):
    if path is None:
        path = f"{get_project_root()}/.eoj"
    start_browser(path)
    click.clear()
