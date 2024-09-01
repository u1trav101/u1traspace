from flask import request
from flask_paginate import Pagination, get_page_args
from config import CONFIG
from db import Query


def users_paginator() -> tuple:
    query = Query()

    filter_online: bool = True if request.args.get("f") == "online" else False
    sort: str | None = request.args.get("s")
    
    number_of_users: int = query.select_users(count=True, online=filter_online)

    page_number: int = int(get_page_args(page_parameter="page")[0])
    users_per_page = CONFIG.USERS_PER_PAGE
    offset: int = (page_number * users_per_page) - users_per_page

    users: list = []
    match sort:
        case "new":
            users = query.select_users(online=filter_online, start=offset, limit=users_per_page)
        case "old":
            users = query.select_users(online=filter_online, start=offset, limit=users_per_page, order="ASC")
        case "mviews":
            users = query.select_users(online=filter_online, start=offset, limit=users_per_page, order_by="page_views")
        case "lviews":
            users = query.select_users(online=filter_online, start=offset, limit=users_per_page, order_by="page_views", order="ASC")
        case _:
            users = query.select_users(online=filter_online, start=offset, limit=users_per_page)

    pagination = Pagination(
        page=page_number,
        per_page=users_per_page,
        total=number_of_users,
        css_framework="bootstrap3"
    )

    return users, page_number, users_per_page, number_of_users, pagination
