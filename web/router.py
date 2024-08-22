from werkzeug import Response
from flask import redirect, url_for
from web.misc import validate_url_vars
import web.misc as misc
import web.routes as routes


def declare_routes(app) -> None:
    @app.before_request
    def before_request() -> None:
        return misc.before_request()

    @app.route("/")
    def index() -> str:
        return routes.index()
    
    @app.route("/set-timezone", methods=["POST"])
    def set_timezone() -> str:
        return routes.set_timezone()

    @app.route("/auth/login/", methods=["GET", "POST"])
    def login() -> Response | str:
        return routes.login()

    @app.route("/auth/logout/")
    def logout() -> Response:
        return routes.logout()

    @app.route("/auth/register/", methods=["GET", "POST"])
    def register() -> Response | str:
        return routes.register()

    @app.route("/user/")
    def user_list() -> Response | str:
        return routes.user_list()

    @app.route("/user/random/")
    def random_user() -> Response:
        return routes.random_user()
    
    @app.route("/news")
    def news() -> Response | str:
        return routes.news()

    @app.route("/user/")
    def redirect_to_user_list() -> Response:
        return redirect(url_for("user_list"))

    @app.route("/user/<user_id>/", methods=["GET", "POST"])
    @validate_url_vars
    def user_profile(user_id: int) -> Response | str | tuple:
        return routes.user_profile(user_id)

    @app.route("/user/<user_id>/blog/")
    @validate_url_vars
    def blog_list(user_id: int) -> Response | str:
        return routes.blog_list(user_id)

    @app.route("/user/<user_id>/blog/<post_id>/", methods=["GET", "POST"])
    @validate_url_vars
    def blog(user_id: int, post_id: int) -> Response | str | tuple:
        return routes.blog(user_id, post_id)

    @app.route("/user/<user_id>/blog/new/", methods=["GET", "POST"])
    @validate_url_vars
    def new_blog(user_id: int) -> Response | str | tuple:
        return routes.new_blog(user_id)

    @app.route("/user/<user_id>/friends/")
    @validate_url_vars
    def friend_list(user_id: int) -> Response | str:
        return routes.friend_list(user_id)

    @app.route("/user/<user_id>/add-friend/", methods=["POST"])
    @validate_url_vars
    def add_friend(user_id: int) -> Response:
        return routes.add_friend(user_id)

    @app.route("/user/<user_id>/remove-friend/", methods=["POST"])
    @validate_url_vars
    def remove_friend(user_id: int) -> Response:
        return routes.remove_friend(user_id)

    @app.route("/preferences/", methods=["GET", "POST"])
    def user_preferences() -> Response | str:
        return routes.user_preferences()

    @app.route("/notifications/", methods=["GET", "POST"])
    def notifications() -> Response | str:
        return routes.notifications()

    # @app.route("/notifications/poll")
    # def notification_poll() -> Response:
    #     return get_notification_counters()

    @app.route("/msg/")
    def message_list() -> Response | str:
        return routes.message_list()

    @app.route("/msg/<user_id>/", methods=["GET", "POST"])
    @validate_url_vars
    def direct_message(user_id: int) -> Response | str:
        return routes.direct_message(user_id)

    @app.route("/msg/<user_id>/poll")
    def message_poll(user_id: int) -> Response | list:
        return routes.message_poll(user_id)

    @app.route("/search/", methods=["GET", "POST"])
    def search() -> str | tuple:
        return routes.search()

    @app.route("/konata/")
    def konata() -> Response:
        return routes.konata()
    
    @app.route("/rss/<request>")
    def rss(request: str) -> Response | str | tuple:
        return routes.rss(request)
    
    @app.route("/faq/")
    def faq() -> str:
        return routes.faq()
