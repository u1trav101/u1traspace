from flask import session, redirect, url_for
from db import Query
from web.misc import render_template
from web.forms import new_blog_form


def new_blog(user_id):
    try:
        int(user_id)
    except ValueError:
        return redirect(url_for("user_profile"))

    if ("user_id") not in session:
        return redirect(url_for("login"))

    elif int(session["user_id"]) != int(user_id):
        return redirect(url_for("user_profile", user_id=user_id))

    form = new_blog_form()
    if form.validate_on_submit():
        query = Query()
        query.insert_blog(user_id, form.title.data, form.corpus.data)
        blog_id = query.select_blogs(limit=1, author_id=user_id)[0]["blog_id"]

        return redirect(url_for("blog", user_id=user_id, post_id=blog_id))

    return render_template(
        "newblog.html",
        form=form
    )
