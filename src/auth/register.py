from werkzeug.security import generate_password_hash
from db import Query


def register_user(email: str, username: str, password: str) -> int:
    query = Query()
    query.insert_user(email, username, generate_password_hash(password))

    new_user: dict = query.select_users(order="DESC", limit=1)[0]

    return new_user["user_id"]
