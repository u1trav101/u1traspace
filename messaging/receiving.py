from db import Query
from markupsafe import Markup
from web.formatting import epoch_to_readable


def get_incoming_senders(recipient_id: int) -> list[dict] | None:
    query = Query()
    res: list = query.select_messages(recipient_id=recipient_id, order="ASC")

    if not res:
        return None

    return res


def get_direct_messages(recipient_id: int, sender_id: int) -> list[dict] | None:
    query = Query()
    res = query.select_messages(recipient_id=recipient_id, sender_id=sender_id)

    if not res:
        return None

    return res


def get_user_conversations(user_id: int) -> list[dict] | None:
    query = Query()
    res: list = query.select_user_conversations(user_id)

    other_users: list = []
    conversations: list[dict] = []

    for i in range(len(res)):
        other_user_id: int | None = None
        message: dict | None = None

        if (res[i]["sender_id"] == user_id) and (
            res[i]["recipient_id"] not in other_users
        ):
            other_user_id = res[i]["recipient_id"]
            message = query.select_messages(
                limit=1, sender_id=user_id, recipient_id=other_user_id
            )[0]

        elif (res[i]["recipient_id"] == user_id) and (
            res[i]["sender_id"] not in other_users
        ):
            other_user_id = res[i]["sender_id"]
            message = query.select_messages(
                limit=1, sender_id=other_user_id, recipient_id=user_id
            )[0]

        if other_user_id and message:
            other_users.append(other_user_id)

            conversations.append(
                {
                    "user_id": other_user_id,
                    "username": query.select_users(user_id=other_user_id, limit=1)[0][
                        "username"
                    ],
                    "corpus": message["corpus"],
                    "date": message["date"],
                }
            )

    conversations = sorted(conversations, key=lambda d: d["date"])

    return conversations


def poll_incoming_messages(
    sender_id: int, recipient_id: int, last_message_id: int = 0
) -> list[dict] | None:
    query = Query()
    sent_messages: list[dict] | None = query.select_messages(
        start=last_message_id,
        sender_id=sender_id,
        recipient_id=recipient_id,
        order="ASC",
    )
    received_messages: list[dict] | None = query.select_messages(
        start=last_message_id,
        sender_id=recipient_id,
        recipient_id=sender_id,
        order="ASC",
    )

    res: list[dict] | None = None
    if received_messages and sent_messages:
        messages = received_messages + sent_messages
        res = sorted(messages, key=lambda m: m["message_id"])
    elif received_messages:
        res = received_messages
    elif sent_messages:
        res = sent_messages

    if res:
        for i in range(len(res)):
            res[i]["date"] = epoch_to_readable(res[i]["date"])
            res[i]["last_seen"] = epoch_to_readable(res[i]["last_seen"])
            res[i]["corpus"] = Markup.escape(res[i]["corpus"])
            res[i].pop("email")
            res[i].pop("password")
            res[i].pop("about")
            res[i].pop("layout")
            res[i].pop("join_date")
            res[i].pop("page_views")
            res[i].pop("private")
            res[i].pop("visible")

    return res
