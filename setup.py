from pathlib import Path
from os import makedirs
from config.config import CONFIG
import tasks


DIRS: list[str] = [
    "./usercontent/img/raw",
    "./usercontent/img/rsz/200px",
    "./usercontent/img/rsz/100px",
    "./usercontent/img/rsz/32px",
    "./usercontent/audio",
    "./usercontent/css",
    "/tmp/u1traspace",
]


def setup() -> None:
    create_dirs()
    if not CONFIG.DEBUG:
        tasks.sync_static()


# create necessary directories
def create_dirs() -> None:
    for directory in DIRS:
        makedirs(Path(directory).resolve(), exist_ok=True)
        with open(Path(Path(directory).resolve() / "stub").resolve(), "w") as stub:
            stub.write("stub")
            stub.close()


if __name__ == "__main__":
    create_dirs()
