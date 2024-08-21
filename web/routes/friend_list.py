from flask import redirect, url_for
from web.misc import render_template
import web.forms as forms
import profile


def friend_list(user_id):
    try:
        int(user_id)
    except ValueError:
        return redirect(url_for("user_list"))

    properties = profile.get_profile_properties(user_id)
    friend_form = forms.friend_form()

    template = "friends.html"
    match properties["layout"]:
        case "twitter":
            template = "twitter/friends.html"
        case "myspace":
            template = "myspace/friends.html"
        case "classic":
            template = "classic/friends.html"

    return render_template(
        template,
        properties=properties,
        blogposts=profile.get_all_user_blogposts(user_id),
        friends=profile.get_user_friends(user_id),
        friend_requests=profile.get_friend_requests(user_id),
        is_friends=profile.is_friends(user_id),
        friend_form=friend_form
    )
