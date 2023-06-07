from werkzeug.security import check_password_hash
from db import Query


def login_correct(id, input_password):
    query = Query()
    user_row = query.get_user_by_id(id)

    if user_row is None:
        return False

    if check_password_hash(user_row["password"], input_password):
        query.update_last_seen(id)
        return True

    return False
