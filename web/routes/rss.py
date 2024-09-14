from flask import url_for, make_response, session
from werkzeug import Response
from feedgen.feed import FeedGenerator
from datetime import datetime
from zoneinfo import ZoneInfo
from web.formatting import epoch_to_readable
from db import Query
from config import CONFIG


def rss(request: str) -> Response | str | tuple:
    fg: FeedGenerator = FeedGenerator()
    fg.logo(CONFIG.CDN_URI + "/static/favicon.gif")
    query = Query()
    posts: list | None = None
    author: str | None = None

    try:
        int(request)
    except ValueError:
        if request != "all":
            return "Invalid RSS request", 400

    if request == "all":
        posts = query.select_blogs()

        fg.id(url_for("index", _external=True))
        fg.title("u1traspace blogs")
        fg.link(href = url_for("index", _external=True))
        fg.author(name = "u1trav101et", email = "enquiries@u1trav101.net")
        fg.description("all blogposts on u1traspace")

    else:
        user_id = int(request)
        posts = query.select_blogs(author_id=int(request))

        if posts:
            users: list = query.select_users(user_id=user_id)
            user: dict | None = users[0] if users else None
            if not user:
                return "That user does not exist", 404

            author = user["username"]
            fg.id(url_for("user.page", user_id=user_id, _external=True))
            fg.title(f"{author} [{user['user_id']}]'s blog")
            fg.link(href = url_for("user.blog.browse", user_id=user_id, _external=True))
            fg.author(name = author, email = "enquiries@u1trav101.net")
            fg.description(f"all of {author}'s blogposts on u1traspace")

    for post in posts:
        blog_url = url_for("user.blog.post", user_id=post["author_id"], post_id=post["blog_id"], _external=True)
        fe = fg.add_entry()
        fe.id(blog_url)
        fe.link(href = blog_url)
        fe.content(content = post["corpus"])
        fe.enclosure(url = f"{CONFIG.CDN_URI}/usercontent/img/rsz/200px/{post['author_id']}.webp", type = "image/webp")

        if request == "all":
            fe.author(name = f"{post['username']} [{post['author_id']}]", email = "enquiries@u1trav101.net")
            fe.title(post['title'])

        else:
            fe.author(name = f"{author} [{post['author_id']}]", email = "enquiries@u1trav101.net")
            fe.title(post['title'])

        fe.published(epoch_to_readable(post["date"], obj=True))

    rss_str = fg.rss_str(pretty = True)
    response = make_response(rss_str)
    response.headers.set("Content-Type", "application/rss+xml")

    return response
