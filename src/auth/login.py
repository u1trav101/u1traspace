from werkzeug.security import check_password_hash
from db import Query
import log


def login_correct(email: str, input_password: str) -> bool:
    query = Query()
    user_rows: list[dict] | None = query.select_users(email=email, limit=1)
    if not user_rows:
        return False

    if check_password_hash(user_rows[0]["password"], input_password):
        log.write(
            __name__,
            f"{user_rows[0]["username"]}[{user_rows[0]["user_id"]}] authenticated...",
        )
        query.update_last_seen(user_rows[0]["user_id"])
        return True

    return False
