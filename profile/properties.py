from db import Query
import os


def get_profile_properties(user_id: int) -> dict | None:
    query = Query()
    res: dict = query.select_users(user_id=user_id, limit=1)[0]

    if not res:
        return None
    
    return res


def get_profile_comments(page_id: int) -> list[dict] | None:
    query = Query()
    res: list = query.select_page_comments(page_id=page_id)

    if not res:
        return None

    return res


def get_profile_css(user_id: int) -> str | None:
    dir_name: str = os.path.dirname(__file__)
    file_path: str = os.path.join(dir_name, f"../usercontent/css/{user_id}.css")

    try:
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        open(file_path, "a").close()
