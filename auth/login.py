from werkzeug.security import check_password_hash
from db import Query


def login_correct(email, input_password):
    query = Query()
    user_row = query.select_users(email=email, limit=1)[0]

    if user_row is None:
        return False

    if check_password_hash(user_row["password"], input_password):
        query.update_last_seen(user_row["user_id"])
        return True

    return False
