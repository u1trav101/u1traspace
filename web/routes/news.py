from werkzeug import Response
from web.overloads import render_template
from db import Query


def news() -> Response | str:
    query = Query()
    blogs: list[dict] | None = None

    blogs = query.select_blogs(limit=20)
    
    return render_template(
        "news.html",
        posts = blogs
    )