from werkzeug.security import generate_password_hash
from db import Query


def register_user(username, password):
    query = Query()
    return query.add_user(username, generate_password_hash(password))
