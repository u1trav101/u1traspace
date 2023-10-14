from flask import url_for, make_response, session
from feedgen.feed import FeedGenerator
from datetime import datetime
from zoneinfo import ZoneInfo
from db import Query

def rss(req_str):
    fg = FeedGenerator()
    fg.logo("https://sys.chiyo.org/static/img/chiyo.png")
    query = Query()
    posts = None
    author = None

    try:
        int(req_str)
    except ValueError:
        if req_str != "all":
            return "Invalid RSS request"

    if req_str == "all":
        posts = query.get_all_blogposts()

        fg.id(url_for("news", _external=True))
        fg.title("All blogs on ChiyoNETOnline")
        fg.link(href = url_for("news", _external=True))
        fg.author(name = "The cool users of ChiyoNETOnline", email = "noreply@chiyo.org")
        fg.description("A collection of all blogs posted by all the users of ChiyoNETOnline")
    
    else:
        posts = query.get_all_user_blogposts(req_str)

        if len(posts) > 0:
            user = query.get_user_by_id(req_str)
            author = user["username"]
            fg.id(url_for("user_profile", user_id=req_str, _external=True))
            fg.title(f"{author} [{user['id']}] blogs on ChiyoNETOnline")
            fg.link(href = url_for("blog_list", user_id=req_str, _external=True))
            fg.author(name = author, email = "noreply@chiyo.org")
            fg.description(f"A collection of all blogs posted by {author} on ChiyoNETOnline")
    
    if len(posts) == 0:
        return "Invalid RSS request"

    for post in posts:
        blog_url = url_for("blog", user_id=post["authorid"], post_id=post["id"], _external=True)
        fe = fg.add_entry()
        fe.id(blog_url)
        fe.link(href = blog_url)
        fe.content(content = post["corpus"])
        fe.enclosure(url = f"http://sys.chiyo.org/usercontent/img/rsz/200px/{post['authorid']}.gif", type = "image/gif")
        
        if req_str == "all":
            fe.author(name = f"{post['username']} [{post['authorid']}]", email = "noreply@chiyo.org")
            fe.title(post['title'])

        else:
            fe.author(name = f"{author} [{post['authorid']}]", email = "noreply@chiyo.org")
            fe.title(post['title'])

        if ("timezone") in session:
            fe.published(datetime.fromtimestamp(int(post["date"]), ZoneInfo(session["timezone"])))
        else:
            fe.published(datetime.fromtimestamp(int(post["date"]), ZoneInfo("Europe/London")))

    rss_str = fg.rss_str(pretty = True)
    response = make_response(rss_str)
    response.headers.set("Content-Type", "application/rss+xml")

    return response
