from datetime import datetime
import os
from eyeofjupyter.config import CONFIG_FILE_NAME, SNAPSHOTS_DIR
from eyeofjupyter.errors import NoProject


def get_project_root():
    cwd = os.getcwd()
    while (parentdir := os.path.dirname(cwd)) != cwd:
        if os.path.isfile(f"{cwd}/{CONFIG_FILE_NAME}"):
            return f"{cwd}/"
        cwd = parentdir
    raise NoProject()


def get_new_snapshot_loc(ipynbfile_path, project_root):
    rel_ipynbfile_path = os.path.relpath(ipynbfile_path, project_root)
    snapshots_base_dir = f"{project_root}/{SNAPSHOTS_DIR}/{rel_ipynbfile_path}/"
    os.makedirs(snapshots_base_dir, exist_ok=True)
    snapshot_version = datetime.now().timestamp()
    return f"{snapshots_base_dir}{snapshot_version}/"


def get_snapshot_report_file(snapshot_version):
    return f"{snapshot_version}report.html"


def get_snapshot_metadatafile(snapshot_version):
    return f"{snapshot_version}metadata.json"
