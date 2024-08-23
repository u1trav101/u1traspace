from flask_wtf import FlaskForm
from werkzeug import Response
from web.misc import render_template
import web.forms as forms
import profile


def _friends(user_id: int) -> Response | str:
    properties: dict = profile.get_profile_properties(user_id)
    friend_form: FlaskForm = forms.friend_form()

    template: str = "friends.html"
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
