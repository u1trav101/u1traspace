from flask_wtf import FlaskForm
from web.overloads import render_template
from web.forms import input_form
import profile


def _browse() -> str:
    pagination_args: tuple = profile.users_paginator()

    return render_template(
        "user/browse.html",
        users = pagination_args[0],
        page = pagination_args[1],
        per_page = pagination_args[2],
        pagination = pagination_args[3],
        total = pagination_args[4],
        forms = {
            "search": input_form()
        }
    )
