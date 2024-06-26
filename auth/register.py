from werkzeug.security import generate_password_hash
from db import Query


def register_user(email, username, password):
    query = Query()
    query.insert_user(
        email, 
        username, 
        generate_password_hash(password)
    )

    return query.select_users(
        order="DESC",
        limit=1
    )[0]["user_id"]
