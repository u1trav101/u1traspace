from db import Query


def send_friend_request(user_id, friend_id):
    query = Query()
    if query.add_friend_request(user_id, friend_id):
        query.add_friend_notification(friend_id, user_id)
