from web.overloads import render_template
from web.forms import input_form
import profile


def browse() -> str:
    pagination: tuple = profile.users_paginator()

    return render_template(
        "user/browse.html",
        pagination={
            "users": pagination[0],
            "current_page": pagination[1],
            "users_per_page": pagination[2],
            "total_users": pagination[3],
            "paginator": pagination[4],
        },
        forms={"search": input_form()},
    )
