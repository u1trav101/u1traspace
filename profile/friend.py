from db import Query


def send_friend_request(user_id, friend_id):
    query = Query()

    pending_reqs = query.get_friend_requests(user_id, friend_id)
    for req in pending_reqs:
        if int(friend_id) == int(req["id"]):
            query.resolve_conflicting_friend_requests(user_id, friend_id)
            return

    if query.add_friend_request(user_id, friend_id):
        query.add_friend_notification(friend_id, user_id)
