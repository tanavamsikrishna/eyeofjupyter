import os
from eyeofjupyter.config import CONFIG_FILE_NAME, SNAPSHOTS_DIR


def get_project_root():
    cwd = os.getcwd()
    while (parentdir := os.path.dirname(cwd)) != cwd:
        if os.path.isfile(f"{cwd}/{CONFIG_FILE_NAME}"):
            return f"{cwd}/"
        cwd = parentdir


def get_new_snapshot_loc(ipynbfile_path):
    rel_ipynbfile_path = os.path.relpath(ipynbfile_path, get_project_root())
    snapshots_base_dir = f"{get_project_root()}/{SNAPSHOTS_DIR}/{rel_ipynbfile_path}/"
    os.makedirs(snapshots_base_dir, exist_ok=True)
    snapshot_base_dir_contents = os.listdir(snapshots_base_dir)
    snapshot_version = 0
    if len(snapshot_base_dir_contents) > 0:
        snapshot_version = (
            max(
                [
                    int(e)
                    for e in snapshot_base_dir_contents
                    if os.path.isdir(f"{snapshots_base_dir}{e}")
                ]
            )
            + 1
        )
    return f"{snapshots_base_dir}{snapshot_version}/"


def get_snapshot_report_file(snapshot_version):
    return f"{snapshot_version}report.html"


def get_snapshot_metadatafile(snapshot_version):
    return f"{snapshot_version}metadata.json"
