from flask import redirect, url_for
import web.misc as misc
import web.routes as routes
from profile import get_notification_counters


def declare_routes(app, captcha):
    @app.before_request
    def before_request():
        return misc.before_request()

    @app.route("/")
    def index():
        return routes.index()
    
    @app.route("/set-timezone", methods=["POST"])
    def set_timezone():
        return routes.set_timezone()

    @app.route("/auth/login/", methods=["GET", "POST"])
    def login():
        return routes.login()

    @app.route("/auth/logout/")
    def logout():
        return routes.logout()

    @app.route("/auth/register/", methods=["GET", "POST"])
    def register(captcha=captcha):
        return routes.register(captcha)

    @app.route("/users/")
    def user_list():
        return routes.user_list()

    @app.route("/users/random/")
    def random_user():
        return routes.random_user()
    
    @app.route("/news")
    def news():
        return routes.news()

    @app.route("/id/")
    def redirect_to_user_list():
        return redirect(url_for("user_list"))

    @app.route("/id/<user_id>/", methods=["GET", "POST"])
    def user_profile(user_id):
        return routes.user_profile(user_id)
    
    @app.route("/id/<user_id>/blog/")
    def blog_list(user_id):
        return routes.blog_list(user_id)

    @app.route("/id/<user_id>/blog/<post_id>/", methods=["GET", "POST"])
    def blog(user_id, post_id):
        return routes.blog(user_id, post_id)

    @app.route("/id/<user_id>/blog/new/", methods=["GET", "POST"])
    def new_blog(user_id):
        return routes.new_blog(user_id)

    @app.route("/id/<user_id>/friends/")
    def friend_list(user_id):
        return routes.friend_list(user_id)

    @app.route("/id/<user_id>/add-friend/", methods=["POST"])
    def add_friend(user_id):
        return routes.add_friend(user_id)

    @app.route("/id/<user_id>/remove-friend/", methods=["POST"])
    def remove_friend(user_id):
        return routes.remove_friend(user_id)

    @app.route("/preferences/", methods=["GET", "POST"])
    def user_preferences():
        return routes.user_preferences()

    @app.route("/notifications/", methods=["GET", "POST"])
    def notifications():
        return routes.notifications()

    @app.route("/notifications/poll")
    def notification_poll():
        return get_notification_counters()

    @app.route("/msg/")
    def message_list():
        return routes.message_list()

    @app.route("/msg/<recipient_id>/", methods=["GET", "POST"])
    def direct_message(recipient_id):
        return routes.direct_message(recipient_id)

    @app.route("/msg/<recipient_id>/poll")
    def message_poll(recipient_id):
        return routes.message_poll(recipient_id)

    @app.route("/search/", methods=["GET", "POST"])
    def search():
        return routes.search()

    @app.route("/konata/")
    def konata():
        return routes.konata()
