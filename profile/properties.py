from db import Query
import os


def get_profile_properties(user_id):
    query = Query()
    res = query.select_users(user_id=user_id, limit=1)[0]

    return res


def get_profile_comments(page_id):
    query = Query()
    res = query.select_page_comments(page_id=page_id)

    return res


def get_profile_css(user_id):
    dir_name = os.path.dirname(__file__)
    file_path = os.path.join(dir_name, f"../usercontent/css/{user_id}.css")

    try:
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        open(file_path, "a").close()


def get_user_friends(user_id):
    query = Query()
    res = query.select_friends(recipient_id=user_id)

    return res
