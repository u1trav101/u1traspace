from random import randint, seed
from datetime import date

from flask_wtf import FlaskForm
from web.misc import render_template
from profile.properties import get_profile_properties
import web.forms as forms
from db import Query


def index() -> str:
    query = Query()
    res: list[dict] = query.select_blogs(limit=6)

    search_form:FlaskForm = forms.search_form()

    number_of_users:int = query.select_users(count=True)
    seed(str(date.today()))
    user_of_the_day: int = randint(0, number_of_users)

    return render_template(
        "index.html",
        new_posts=res,
        form=search_form,
        user_of_the_day=user_of_the_day,
        user=get_profile_properties(user_of_the_day)
    )
