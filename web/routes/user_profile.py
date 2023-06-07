from flask import session, redirect, url_for, request
from db import Query
from web.misc import render_template
import web.forms as forms
import profile
import messaging


def user_profile(user_id):
    try:
        int(user_id)
    except ValueError:
        return redirect(url_for("user_list"))

    properties = profile.get_profile_properties(user_id)
    if not properties:
        return redirect(url_for("user_list"))

    comment_form = forms.comment_form()
    delete_form = forms.comment_delete_form()
    friend_form = forms.friend_form()
    query = Query()

    if ("user_id") in session:
        if comment_form.validate_on_submit():
            messaging.send_profile_comment(
                session["user_id"],
                user_id,
                comment_form.corpus.data
            )

        elif delete_form.validate_on_submit():
            comment_id = request.form.get("delete")
            res = str(query.get_user_comment_author(user_id, comment_id))

            if (session["user_id"] == user_id) or (session["user_id"] == res):
                query.delete_user_comment(user_id, comment_id)

                return redirect(url_for("user_profile", user_id=user_id))

        if request.method == "POST":
            return redirect(url_for("user_profile", user_id=user_id))


    query.update_page_views(user_id)

    template = "profile.html"
    match properties["interface"]:
        case "twitter":
            template = "twitter/profile.html"
        case "classic":
            template = "classic/profile.html"
        case "myspace":
            template = "myspace/profile.html"

    return render_template(
        template,
        properties=properties,
        comments=profile.get_profile_comments(user_id),
        blogposts=profile.get_all_user_blogposts(user_id),
        friends=profile.get_user_friends(user_id),
        comment_form=comment_form,
        delete_form=delete_form,
        friend_form=friend_form
    )
