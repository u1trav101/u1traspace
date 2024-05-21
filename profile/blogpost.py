from db import Query


def get_blogpost(user_id, post_id):
    query = Query()
    res = query.get_blogpost(user_id, post_id)

    if not res:
        return None

    return res


def get_blogpost_comments(user_id, post_id):
    query = Query()
    res = query.get_blogpost_comments(user_id, post_id)

    if not res:
        return None

    return res


def get_all_user_blogposts(author_id):
    query = Query()
    res = query.select_blogs(author_id=author_id)

    return res
