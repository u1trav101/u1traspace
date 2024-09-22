from flask import url_for, make_response
from werkzeug import Response
from feedgen.feed import FeedGenerator
from web.formatting import epoch_to_readable
from db import Query
from config import CONFIG
from web.utils import get_image_size


def rss(request: str) -> Response | str | tuple:
    fg: FeedGenerator = FeedGenerator()
    fg.logo(CONFIG.CDN_URI + "/static/favicon.ico")

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
        fg.link(href=url_for("index", _external=True))
        fg.author(name="u1trav101et", email="enquiries@u1trav101.net")
        fg.description("all blogposts on u1traspace")

    else:
        user_id = int(request)
        posts = query.select_blogs(author_id=int(request))

        users: list = query.select_users(user_id=user_id)
        user: dict | None = users[0] if users else None
        if not user:
            return "That user does not exist", 404

        author = user["username"]
        fg.id(url_for("user.page", user_id=user_id, _external=True))
        fg.title(f"{author} [{user['user_id']}]'s blog")
        fg.link(href=url_for("user.blog.browse", user_id=user_id, _external=True))
        fg.author(name=author, email="enquiries@u1trav101.net")
        fg.description(f"all of {author}'s blogposts on u1traspace")

    for post in posts:
        fe = fg.add_entry()

        blog_url = url_for(
            "user.blog.post",
            user_id=post["author_id"],
            post_id=post["blog_id"],
            _external=True,
        )
        image_size = get_image_size(
            f"{CONFIG.CDN_URI}/usercontent/img/rsz/200px/{post['author_id']}.webp"
        )

        fe.id(blog_url)
        fe.link(href=blog_url)
        fe.content(post["corpus"], type="CDATA")

        if image_size > 0:
            fe.enclosure(
                url=f"{CONFIG.CDN_URI}/usercontent/img/rsz/200px/{post['author_id']}.webp",
                type="image/webp",
                length=str(image_size),
            )
        else:
            fe.enclosure(
                url=f"{CONFIG.CDN_URI}/usercontent/img/rsz/200px/default.webp",
                type="image/webp",
                length="18354",
            )

        if request == "all":
            fe.author(
                name=f"{post['username']} [{post['author_id']}]",
                email="enquiries@u1trav101.net",
            )
            fe.title(post["title"])
        else:
            fe.author(
                name=f"{author} [{post['author_id']}]", email="enquiries@u1trav101.net"
            )
            fe.title(post["title"])

        fe.published(epoch_to_readable(post["date"], obj=True))

    rss_str = fg.atom_str(pretty=True)
    response = make_response(rss_str)
    response.headers.set("Content-Type", "application/rss+xml")

    return response
