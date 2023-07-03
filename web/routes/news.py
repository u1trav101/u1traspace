from web.misc import render_template
from db import Query


def news():
    query = Query()
    blogs = query.get_all_blogposts(20)
    
    return render_template(
        "news.html",
        new_posts=blogs
    )