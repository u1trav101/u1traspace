from cdn import ls
from pathlib import Path
from datetime import datetime, timezone
from os.path import getmtime
from cdn import upload

static_files: list[str] = []


def sync_folder(path: str, recursive: bool = False) -> None:
    res: list = ls(path)
    if res:
        if "Contents" in res:
            for file in res.get("Contents"):
                static_files.append(file)
        if "CommonPrefixes" in res:
            for folder in res.get("CommonPrefixes"):
                if recursive:
                    sync_folder(folder["Prefix"], recursive)


def sync_static():
    print("Syncing static files with CDN")

    sync_folder("u1traspace/static/css/", True)

    for file in static_files:
        local_file = Path("static/" + file.get("Key")[18:])
        local_mtime = datetime.fromtimestamp(getmtime(local_file.resolve())).astimezone(
            timezone.utc
        )

        remote_mtime = file.get("LastModified")

        if local_mtime.timestamp() > remote_mtime.timestamp():
            print(f"{file.get("Key")} is out of date. Syncing...")
            upload(local_file.resolve(), file.get("Key"))
            print(f"{file.get("Key")} synced.")

    print("DONE")
