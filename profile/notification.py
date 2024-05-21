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

    profile_comment_approvals = query.select_page_comments(approved=False, page_id=user_id)
    blog_comment_approvals = query.select_pending_blog_comments(author_id=user_id)
    friend_request_approvals = query.select_friends(approved=False, recipient_id=user_id)
    unseen_messages = query.select_messages(read=False, recipient_id=user_id)

    return profile_comment_approvals + blog_comment_approvals + friend_request_approvals + unseen_messages
