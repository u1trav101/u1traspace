from flask import session
from db import Query


# returns True when redirecting to friend_list, returns False when redirecting to recipient's page
def send_friend_request(sender_id: int, recipient_id: int) -> bool:
    query = Query()

    pending_sent: list[dict] = query.select_friends(
        sender_id=sender_id, recipient_id=recipient_id, approved=None
    )
    pending_received: list[dict] = query.select_friends(
        sender_id=recipient_id, recipient_id=sender_id, approved=None
    )

    if pending_sent:
        for pending in pending_sent:
            if (
                pending["recipient_id"] == recipient_id
            ):  # sender has already sent a request so no further action is needed
                return False

    if (
        pending_received and not pending_received[0]["approved"]
    ):  # approve friend request already sent by recipient
        query.update_friend(
            sender_id=recipient_id, recipient_id=sender_id, approved=True
        )
        return True
    elif pending_received:  # users are already friends so no further action is needed
        return True

    # creates a friend request
    query.insert_friend(sender_id=sender_id, recipient_id=recipient_id)
    return False


def get_user_friends(user_id: int, approved: bool | None = True) -> list[dict] | None:
    query = Query()

    res: list = query.select_friends(
        sender_id=user_id, approved=approved
    ) + query.select_friends(recipient_id=user_id, approved=approved)

    if not res:
        return None

    return res


def get_friend_requests(user_id: int) -> list[dict] | None:
    query = Query()

    res: list = query.select_friends(recipient_id=user_id, approved=False)

    if not res:
        return None

    return res


def is_friends(user_id: int) -> bool | str:
    if ("user_id") not in session:
        return False

    friends = get_user_friends(user_id, None)
    if friends:
        for friend in friends:
            if (friend["sender_id"] == int(session["user_id"])) or (
                friend["recipient_id"] == int(session["user_id"])
            ):
                return True if friend["approved"] is True else "pending"

    return False
