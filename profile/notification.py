from flask import session, redirect, url_for
from db import Query


def get_notification_counters():
    if ("user_id") not in session:
        return redirect(url_for("login"))
    
    query = Query()

    return {
        "profile_comment_approval": query.select_page_comments(count=True, approved=False, page_id=session["user_id"])[0]["COUNT(*)"],
        "blog_comment_approval": query.select_pending_blog_comments(count=True, author_id=session["user_id"])[0]["COUNT(*)"],
        "friend_request_approval": query.select_friends(count=True, approved=False, recipient_id=session["user_id"])[0]["COUNT(*)"],
        "unseen_message": query.select_messages(count=True, read=False, recipient_id=session["user_id"])[0]["COUNT(*)"]
    }

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
                        notification["actionpostid"],
                        session["user_id"]
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
