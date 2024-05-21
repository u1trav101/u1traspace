from flask import redirect, url_for
from profile import random

def random_user():
    return redirect(url_for(
        "user_profile",
        user_id=random()["user_id"]
    ))
