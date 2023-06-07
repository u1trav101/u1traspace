from flask import session, redirect, url_for, request
from web.misc import render_template
from db import Query
import web.forms as forms
import profile
import messaging


def blog(user_id, post_id):
    try:
        int(user_id)
    except ValueError:
        return redirect(url_for("user_list"))

    try:
        int(post_id)
    except ValueError:
        return redirect(url_for("blog_list", user_id=user_id))

    blogpost = profile.get_blogpost(user_id, post_id)
    if not blogpost:
        return redirect(url_for("blog_list", user_id=user_id))

    comment_form = forms.comment_form()
    delete_form = forms.comment_delete_form()
    friend_form = forms.friend_form()

    if ("user_id") in session:
        if comment_form.validate_on_submit():
            messaging.send_blog_comment(
                session["user_id"], user_id, post_id, comment_form.corpus.data)

        elif delete_form.validate_on_submit():
            delete_value = request.form.get("delete")
            query = Query()

            if delete_value == "blog":
                query.delete_blogpost(user_id, post_id)

                return redirect(url_for("user_profile", user_id=user_id))

            res = str(query.get_blog_comment_author(
                user_id,
                post_id,
                delete_value
            ))

            if (session["user_id"] == user_id) or (session["user_id"] == res):
                query.delete_blog_comment(post_id, delete_value)

                return redirect(url_for(
                    "blog",
                    user_id=user_id,
                    post_id=post_id
                ))

        if request.method == "POST":
            return redirect(url_for("blog", user_id=user_id, post_id=post_id))

    properties = profile.get_profile_properties(user_id)
    template = "blogpost.html"
    match properties["interface"]:
        case "twitter":
            template = "twitter/blogpost.html"
        case "classic":
            template = "classic/blogpost.html"
        case "myspace":
            template = "myspace/blogpost.html"

    return render_template(
        template,
        properties=properties,
        blogpost=blogpost,
        blogposts=profile.get_all_user_blogposts(user_id),
        comments=profile.get_blogpost_comments(user_id, post_id),
        friends=profile.get_user_friends(user_id),
        comment_form=comment_form,
        delete_form=delete_form,
        friend_form=friend_form
    )
