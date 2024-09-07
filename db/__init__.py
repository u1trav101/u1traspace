import mariadb
from config import CONFIG
from db.queries import _Query


def __setup() -> None:
    try:
        return mariadb.connect(
            user=CONFIG.MARIADB_USER,
            password=CONFIG.MARIADB_PASSWORD,
            host=CONFIG.MARIADB_HOST,
            port=CONFIG.MARIADB_PORT,
            database=CONFIG.MARIADB_DATABASE
        )
    except:
        print("Error connecting to MariaDB platform")


def Query() -> _Query:
    return _Query(__setup())
