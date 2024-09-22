from werkzeug.security import generate_password_hash
from db import Query
import log


def register_user(email: str, username: str, password: str) -> int:
    query = Query()
    query.insert_user(email, username, generate_password_hash(password))

    new_user: dict = query.select_users(order="DESC", limit=1)[0]
    log.write(
        __name__,
        f"new user {new_user["username"]}[{new_user["user_id"]}] registered...",
    )

    return new_user["user_id"]
