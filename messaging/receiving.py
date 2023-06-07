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
