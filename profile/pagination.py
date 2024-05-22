from flask import request
from flask_paginate import Pagination, get_page_args
from db import Query


def users_paginator():
    query = Query()

    filter_online = True if request.args.get("show") == "online" else False

    number_of_users = query.select_users(count=True)

    page_number = get_page_args(page_parameter="page")[0]
    users_per_page = 15
    offset = (page_number * 15) - 15
    users = query.select_users(online=filter_online, start=offset)

    pagination = Pagination(
        page=page_number,
        per_page=users_per_page,
        total=number_of_users,
        css_framework="bootstrap3"
    )

    return users, page_number, users_per_page, pagination, number_of_users
