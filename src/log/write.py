from pathlib import Path
from datetime import datetime


LOG_PATH = "../logs/u1traspace.log"


def write(module: str, msg: str) -> None:
    number_of_lines: int = 0
    time: datetime = datetime.now()
    time_str: str = datetime.strftime(time, "%d/%m/%y %H:%M:%S")

    try:
        with open(Path(LOG_PATH).resolve(), "r") as log:
            number_of_lines = len(log.readlines())
    except FileNotFoundError:
        pass

    with open(LOG_PATH, "a") as log:
        log.write(
            f"{'\n' if number_of_lines != 0 else ''}({time_str}) [{module}] {msg}"
        )
