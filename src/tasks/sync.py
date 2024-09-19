from cdn import ls
from pathlib import Path
from datetime import datetime, timezone
from os.path import getmtime
from cdn import upload
import log

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
    log.write(__name__, "syncing static files with cdn...")

    log.write(__name__, "checking modification dates of cdn static files...")
    sync_folder("u1traspace/static/css/", True)
    log.write(__name__, "checking modification dates of cdn static files... DONE")

    log.write(__name__, "checking modification dates of local static files...")
    for file in static_files:
        local_file = Path("static/" + file.get("Key")[18:])
        local_mtime = datetime.fromtimestamp(getmtime(local_file.resolve())).astimezone(
            timezone.utc
        )

        remote_mtime = file.get("LastModified")

        if local_mtime.timestamp() > remote_mtime.timestamp():
            log.write(
                __name__,
                f"{file.get("Key")} is out of date. uploading local version...",
            )

            upload(local_file.resolve(), file.get("Key"))

            log.write(
                __name__,
                f"{file.get("Key")} is out of date. uploading local version... DONE",
            )

    log.write(__name__, "checking modification dates of local static files... DONE")
    log.write(__name__, "syncing static files with cdn... DONE")
