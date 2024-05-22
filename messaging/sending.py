from db import Query


def send_profile_comment(author_id, profile_id, corpus):
    query = Query()
    query.insert_page_comment(profile_id, author_id, corpus)


def send_blog_comment(author_id, blog_id, corpus):
    query = Query()
    query.insert_blog_comment(blog_id, author_id, corpus)


def send_message(sender_id, recipient_id, corpus):
    query = Query()
    query.insert_message(sender_id, recipient_id, corpus)
