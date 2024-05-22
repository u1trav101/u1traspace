from db import Query


def get_blogpost(user_id, post_id):
    query = Query()
    res = query.select_blogs(author_id=user_id, blog_id=post_id)

    if not res:
        return None

    return res[0]


def get_blogpost_comments(post_id):
    query = Query()
    res = query.select_blog_comments(blog_id=post_id)

    if not res:
        return None

    return res


def get_all_user_blogposts(author_id):
    query = Query()
    res = query.select_blogs(author_id=author_id)

    return res
