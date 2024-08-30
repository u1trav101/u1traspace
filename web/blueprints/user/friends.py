from flask_wtf import FlaskForm
from werkzeug import Response
from web.overloads import render_template
import web.forms as forms
import profile


def _friends(user_id: int) -> Response | str:
    properties: dict = profile.get_profile_properties(user_id)
    friend_form: FlaskForm = forms.friend_form()

    template: str = "user/friends.html"
    match properties["layout"]:
        case "twitter":
            template = "twitter/user/friends.html"
        case "myspace":
            template = "myspace93/user/friends.html"

    return render_template(
        template,
        properties=properties,
        blogposts=profile.get_all_user_blogposts(user_id),
        friends=profile.get_user_friends(user_id),
        friend_requests=profile.get_friend_requests(user_id),
        is_friends=profile.is_friends(user_id),
        friend_form=friend_form
    )
