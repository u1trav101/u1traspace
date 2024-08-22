from flask import request
from flask_paginate import Pagination, get_page_args
from db import Query


def users_paginator() -> tuple:
    query = Query()

    filter_online: bool = True if request.args.get("f") == "online" else False
    sort: str | None = request.args.get("s")
    
    number_of_users: int = query.select_users(count=True, online=filter_online)

    page_number: int = int(get_page_args(page_parameter="page")[0])
    users_per_page = 15
    offset: int = (page_number * 15) - 15

    users: list = []
    match sort:
        case "new":
            users = query.select_users(online=filter_online, start=offset)
        case "old":
            users = query.select_users(online=filter_online, start=offset, order="ASC")
        case "mviews":
            users = query.select_users(online=filter_online, start=offset, order_by="page_views")
        case "lviews":
            users = query.select_users(online=filter_online, start=offset, order_by="page_views", order="ASC")
        case _:
            users = query.select_users(online=filter_online, start=offset)

    pagination = Pagination(
        page=page_number,
        per_page=users_per_page,
        total=number_of_users,
        css_framework="bootstrap3"
    )

    return users, page_number, users_per_page, pagination, number_of_users
