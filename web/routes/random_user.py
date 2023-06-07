from flask import redirect, url_for
from db import Query


def random_user():
    query = Query()
    return redirect(url_for(
        "user_profile",
        user_id=query.get_random_user_profile()
    ))
