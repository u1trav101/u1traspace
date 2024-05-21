from db import Query
from markupsafe import Markup
from web.misc import unix_to_readable


def get_incoming_senders(recipient_id):
    query = Query()
    res = query.get_message_senders(recipient_id)

    return res


def get_direct_messages(recipient_id, sender_id):
    query = Query()
    res = query.get_all_user_messages(recipient_id, sender_id)

    return res

def get_user_conversations(user_id):
    query = Query()
    res = query.select_user_conversations(user_id)

    user_id = int(user_id)
    other_users = []
    conversations = []

    for i in range(len(res)):
        other_user_id = None

        if (res[i]["senderid"] == user_id) and (res[i]["recipientid"] not in other_users):
            other_user_id = res[i]["recipientid"]

        elif (res[i]["recipientid"] == user_id) and (res[i]["senderid"] not in other_users):
            other_user_id = res[i]["senderid"]
        
        if other_user_id:
            other_users.append(other_user_id)

            message = query.select_messages(limit=1, sender_id=user_id, recipient_id=other_user_id)

            conversations.append({
                "id": other_user_id,
                "username": query.get_user_by_id(other_user_id)["username"],
                "sender_id": message["senderid"],
                "sender_username": query.get_user_by_id(message["senderid"])["username"],
                "corpus": message["corpus"],
                "date": message["date"]
            })
    
    conversations = sorted(conversations, key=lambda d: d["date"], reverse=True)

    return conversations


def poll_incoming_messages(sender_id, recipient_id, last_message_id):
    query = Query()
    res = query.poll_incoming_messages(sender_id, recipient_id, last_message_id)

    if not res:
        return [False]

    else:
        res.insert(0, True)
        for i in range(1, len(res)):
            res[i]["date"] = unix_to_readable(res[i]["date"], True)
            res[i]["corpus"] = Markup.escape(res[i]["corpus"])

    return res
