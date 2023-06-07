from flask import session, redirect, url_for
from db import Query


def get_notification_counters():
    if ("user_id") not in session:
        return redirect(url_for("login"))

    notifications = None
    if ("user_id") in session:
        query = Query()
        notifications = query.get_user_notification_types(session["user_id"])

    notification_counters = {
        "profile_comment_approval": 0,
        "blog_comment_approval": 0,
        "friend_request_approval": 0,
        "unseen_message": 0
    }
    for notification in notifications:
        notification_counters[notification["type"]] += 1

    return notification_counters


def get_all_notifications(user_id):
    query = Query()
    notifications = query.get_user_notifications(user_id)

    for notification in notifications:
        match notification["type"]:
            case "profile_comment_approval":
                notification.update({
                    "comment": query.get_user_comment(
                        notification["actioncommentid"],
                        user_id
                    )
                })

            case "blog_comment_approval":
                notification.update({
                    "comment": query.get_blogpost_comment(
                        notification["actionuserid"],
                        notification["actioncommentid"],
                        notification["actionpostid"]
                    ),
                    "blog": query.get_blogpost(
                        user_id,
                        notification["actionpostid"]
                    )
                })

            case "friend_request_approval":
                notification.update({
                    "username": query.get_user_by_id(
                        notification["actionuserid"]
                    )["username"]
                })

            case "unseen_message":
                notification.update({
                    "username": query.get_user_by_id(
                        notification["actionuserid"]
                    )["username"]
                })

    return notifications
