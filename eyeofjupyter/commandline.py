from datetime import datetime
import json
import os
import click
from nbconvert import HTMLExporter

from eyeofjupyter.fs_format import (
    get_new_snapshot_loc,
    get_snapshot_metadatafile,
    get_snapshot_report_file,
)


@click.group()
def cli():
    pass


@cli.command()
@click.argument("ipynbfile", type=click.Path(exists=True, readable=True))
def take_snapshot(ipynbfile):
    ipynbfile = f"{os.getcwd()}/{ipynbfile}"
    new_snapshot_version_loc = get_new_snapshot_loc(ipynbfile)
    os.makedirs(new_snapshot_version_loc)

    he = HTMLExporter()
    (body, _resources) = he.from_file(ipynbfile)
    metadata = {"snapshot datetime": datetime.now().isoformat()}
    with open(get_snapshot_report_file(new_snapshot_version_loc), "w+") as f:
        f.write(body)
    with open(get_snapshot_metadatafile(new_snapshot_version_loc), "w+") as f:
        json.dump(metadata, f)


@cli.command
def browse():
    pass
