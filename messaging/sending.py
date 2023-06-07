from db import Query


def send_profile_comment(author_id, profile_id, corpus):
    query = Query()
    query.add_profile_comment(author_id, profile_id, corpus)


def send_blog_comment(author_id, page_id, blog_id, corpus):
    query = Query()
    query.add_blog_comment(author_id, page_id, blog_id, corpus)


def send_message(sender_id, recipient_id, corpus):
    query = Query()
    query.add_message(sender_id, recipient_id, corpus)
