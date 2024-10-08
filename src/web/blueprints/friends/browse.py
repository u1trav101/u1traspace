from werkzeug import Response
from web.overloads import render_template
from web.forms import blank_form
import profile


def browse(user_id: int) -> Response | str:
    properties: dict = profile.get_profile_properties(user_id)

    template: str = "friend/browse.html"
    match properties["layout"]:
        case "twitter":
            template = "twitter/friend/browse.html"
        case "myspace":
            template = "myspace93/friend/browse.html"

    return render_template(
        template,
        properties=properties,
        blogposts=profile.get_all_user_blogposts(user_id),
        friends=profile.get_user_friends(user_id),
        friend_requests=profile.get_friend_requests(user_id),
        is_friends=profile.is_friends(user_id),
        forms={"friend": blank_form()},
    )
