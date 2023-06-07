from flask import request
from flask_paginate import Pagination, get_page_args
from db import Query


def users_paginator():
    query = Query()

    filter_online = False
    if request.args.get("show") == "online":
        filter_online = True

    number_of_users = query.get_number_of_users(filter_online)

    page_number = get_page_args(page_parameter="page")[0]
    users_per_page = 15
    offset = (page_number * 15) - 15
    users = query.get_list_of_users(offset, filter_online)

    pagination = Pagination(
        page=page_number,
        per_page=users_per_page,
        total=number_of_users,
        css_framework="bootstrap3"
    )

    return users, page_number, users_per_page, pagination, number_of_users
