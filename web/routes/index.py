from datetime import date
from web.overloads import render_template
from profile.properties import get_profile_properties
from db import Query


def index() -> str:
    query = Query()

    try:
        user_of_the_day: list[dict] = query.select_users(limit=1, random=True, seed=int(date.today().strftime("%d%m%Y")))[0]
        return render_template(
            "index.html",
            user_of_the_day = user_of_the_day,
            user = get_profile_properties(user_of_the_day["user_id"])
        )
    except IndexError:
        return render_template("index.html")

