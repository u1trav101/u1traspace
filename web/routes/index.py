from random import randint, seed
from datetime import date
from web.overloads import render_template
from profile.properties import get_profile_properties
from db import Query


def index() -> str:
    query = Query()
    res: list[dict] = query.select_blogs(limit=6)

    number_of_users:int = query.select_users(count=True)
    seed(str(date.today()))
    user_of_the_day: int = randint(0, number_of_users)

    return render_template(
        "index.html",
        new_posts = res,
        user_of_the_day = user_of_the_day,
        user = get_profile_properties(user_of_the_day)
    )
