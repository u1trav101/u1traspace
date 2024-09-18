from db import Query


def random() -> dict:
    query = Query()
    return query.select_users(limit=1, random=True)[0]
