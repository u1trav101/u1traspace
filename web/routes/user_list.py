from flask_wtf import FlaskForm
from web.misc import render_template
import web.forms as forms
import profile


def user_list() -> str:
    pagination_args: tuple = profile.users_paginator()
    search_form: FlaskForm = forms.search_form()

    return render_template(
        "users.html",
        users=pagination_args[0],
        page=pagination_args[1],
        per_page=pagination_args[2],
        pagination=pagination_args[3],
        total=pagination_args[4],
        form=search_form
    )
