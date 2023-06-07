from celery import shared_task
from db import Query


@shared_task
def handle_notification(res):
    action_array = res.split(",")

    query = Query()
    notification = query.get_user_notification(action_array[1])
    query.delete_user_notification(action_array[1])

    state = 1
    if action_array[0] == "delete":
        state = 0

    match notification["type"]:
        case "profile_comment_approval":
            query.user_comment_action(
                state,
                notification["actioncommentid"],
                notification["userid"]
            )

        case "blog_comment_approval":
            query.blogpost_comment_action(
                state,
                notification["actioncommentid"],
                notification["actionuserid"],
                notification["userid"],
                notification["actionpostid"]
            )

        case "friend_request_approval":
            if action_array[0] == "accept":
                query.friend_approve_action(
                    notification["userid"],
                    notification["actionuserid"]
                )
            elif action_array[0] == "reject":
                query.friend_reject_action(
                    notification["userid"],
                    notification["actionuserid"]
                )


@shared_task
def clear_message_notifications(user_id, recipient_id):
    query = Query()
    query.clear_message_notifications(user_id, recipient_id)
