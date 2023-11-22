from datetime import datetime
from json import dump as json_dump
from os import makedirs
import click
from shutil import copyfile
from os.path import basename

from eyeofjupyter.fs_format import (
    get_new_snapshot_loc,
    get_project_root,
    get_snapshot_metadatafile,
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
    makedirs(new_snapshot_version_loc)

    copyfile(ipynbfile, f"{new_snapshot_version_loc}{basename(ipynbfile)}")

    metadata = {"snapshot datetime": datetime.now().isoformat()}
    with open(get_snapshot_metadatafile(new_snapshot_version_loc), "w+") as f:
        json_dump(metadata, f)


@cli.command()
@click.option("--path", type=click.Path(resolve_path=True))
def browse(path):
    if path is None:
        path = f"{get_project_root()}.eoj"
    start_browser(path)
    click.clear()
