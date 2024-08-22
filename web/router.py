from werkzeug import Response
from flask import redirect, url_for
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
    def user_profile(user_id: str) -> Response | str:
        return routes.user_profile(int(user_id))
    
    @app.route("/user/<user_id>/blog/")
    def blog_list(user_id: str) -> Response | str:
        return routes.blog_list(int(user_id))

    @app.route("/user/<user_id>/blog/<post_id>/", methods=["GET", "POST"])
    def blog(user_id: str, post_id: str) -> Response | str:
        try:
            int(user_id)
        except ValueError:
            return redirect(url_for("user_list"))
        try:
            int(post_id)
        except ValueError:
            return redirect(url_for("blog_list", user_id=user_id))
        
        return routes.blog(int(user_id), int(post_id))

    @app.route("/user/<user_id>/blog/new/", methods=["GET", "POST"])
    def new_blog(user_id: str) -> Response | str:
        return routes.new_blog(int(user_id))

    @app.route("/user/<user_id>/friends/")
    def friend_list(user_id: str) -> Response | str:
        return routes.friend_list(int(user_id))

    @app.route("/user/<user_id>/add-friend/", methods=["POST"])
    def add_friend(user_id: str) -> Response:
        return routes.add_friend(int(user_id))

    @app.route("/user/<user_id>/remove-friend/", methods=["POST"])
    def remove_friend(user_id: str) -> Response:
        return routes.remove_friend(int(user_id))

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

    @app.route("/msg/<recipient_id>/", methods=["GET", "POST"])
    def direct_message(recipient_id: str) -> Response | str:
        return routes.direct_message(int(recipient_id))

    @app.route("/msg/<recipient_id>/poll")
    def message_poll(recipient_id: str) -> Response | list:
        return routes.message_poll(int(recipient_id))

    @app.route("/search/", methods=["GET", "POST"])
    def search() -> str:
        return routes.search()

    @app.route("/konata/")
    def konata() -> Response:
        return routes.konata()
    
    @app.route("/rss/<req_str>")
    def rss(request: str) -> Response | str:
        return routes.rss(request)
    
    @app.route("/faq/")
    def faq() -> str:
        return routes.faq()
