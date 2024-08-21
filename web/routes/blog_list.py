from flask import redirect, url_for
from web.misc import render_template
from web.forms import friend_form
import profile


def blog_list(user_id):
    try:
        int(user_id)
    except ValueError:
        return redirect(url_for("user_list"))

    form = friend_form()

    return render_template(
        "bloglist.html",
        properties=profile.get_profile_properties(user_id),
        blogposts=profile.get_all_user_blogposts(user_id),
        friends=profile.get_user_friends(user_id),
        is_friends=profile.is_friends(user_id),
        friend_form=form
    )
