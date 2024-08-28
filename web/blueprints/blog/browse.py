from werkzeug import Response
from web.overloads import render_template
from web.forms import friend_form
import profile


def _browse(user_id: int) -> Response | str:
    form = friend_form()

    return render_template(
        "blog/browse.html",
        properties=profile.get_profile_properties(user_id),
        blogposts=profile.get_all_user_blogposts(user_id),
        friends=profile.get_user_friends(user_id),
        is_friends=profile.is_friends(user_id),
        friend_form=form
    )
