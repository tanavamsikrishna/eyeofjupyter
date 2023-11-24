import os

CONFIG_FILE_NAME = "eoj.toml"
SNAPSHOTS_DIR = ".eoj"
METADATA_FILE = "metadata.json"
SNAPSHOT_FILE_NAME = "snapshot.ipynb"
DEBUG = os.getenv("EOJ_DEBUG") == "true"
PORT = 8080
