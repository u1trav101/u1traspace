import db.users as users
import db.page_comments as page_comments
import db.blogs as blogs
import db.blog_comments as blog_comments
import db.friends as friends
import db.messages as messages
from config import CONFIG


class _Query():
    def __init__(self, conn):
        self.conn = conn
        self.cur = conn.cursor(dictionary=True)

    def __del__(self):
        self.conn.commit()
        self.conn.close()
    
    # works on users table
    def select_users(self, count=False, online=False, start=0, visible=True, order="ASC", limit=CONFIG.SELECT_LIMIT, email=None, user_id=None):
        return users.select_users(
            self.cur, 
            count=count, 
            online=online, 
            start=start, 
            visible=visible,
            order=order,
            limit=limit,
            email=email,
            user_id=user_id
        )
    
    def search_users(self, search_term):
        return users.search_users(
            self.cur,
            search_term=search_term
        )
    
    def insert_user(self, email, username, password):
        users.insert_user(
            self.cur,
            email=email, 
            username=username, 
            password=password
        )
    
    def update_user(self, user_id, about=None, layout=None, private=None):
        users.update_user(
            self.cur,
            user_id=user_id,
            about=about,
            layout=layout,
            private=private
        )
    
    def update_last_seen(self, user_id):
        self.cur.callproc("update_last_seen", [user_id])
    
    def increase_page_views(self, user_id):
        self.cur.callproc("increase_page_views", [user_id])
    
    # works on page_comments table
    def select_page_comments(self, count=False, visible=True, approved=True, order="DESC", limit=CONFIG.SELECT_LIMIT, comment_id=None, page_id=None, author_id=None):
        return page_comments.select_page_comments(
            self.cur,
            count=count,
            visible=visible,
            approved=approved,
            order=order,
            limit=limit,
            comment_id=comment_id,
            page_id=page_id,
            author_id=author_id
        )
    
    def insert_page_comment(self, page_id, author_id, corpus):
        page_comments.insert_page_comment(
            self.cur,
            page_id=page_id,
            author_id=author_id,
            corpus=corpus
        )

    # works on blogs table
    def select_blogs(self, count=False, visible=True, order="DESC", limit=CONFIG.SELECT_LIMIT, blog_id=None, author_id=None):
        return blogs.select_blogs(
            self.cur,
            count=count,
            visible=visible,
            order=order,
            limit=limit,
            blog_id=blog_id,
            author_id=author_id
        )
    
    def search_blogs(self, search_term):
        return blogs.search_blogs(
            self.cur,
            search_term=search_term
        )
    
    def insert_blog(self, author_id, title, corpus):
        blogs.insert_blog(
            self.cur,
            author_id=author_id,
            title=title,
            corpus=corpus
        )
    
    # works on blog_comments table
    def select_blog_comments(self, count=False, visible=True, approved=True, order="DESC", limit=CONFIG.SELECT_LIMIT, comment_id=None, blog_id=None, author_id=None):
        return blog_comments.select_blog_comments(
            self.cur,
            count=count,
            visible=visible,
            approved=approved,
            order=order,
            limit=limit,
            comment_id=comment_id,
            blog_id=blog_id,
            author_id=author_id
        )
    
    def select_pending_blog_comments(self, count=False, visible=True, order="DESC", limit=CONFIG.SELECT_LIMIT, blog_id=None, author_id=None):
        return blog_comments.select_pending_blog_comments(
            self.cur,
            count=count,
            visible=visible,
            order=order,
            limit=limit,
            blog_id=blog_id,
            author_id=author_id
        )
    
    def insert_blog_comment(self, blog_id, author_id, corpus):
        blog_comments.insert_blog_comment(
            self.cur,
            blog_id=blog_id,
            author_id=author_id,
            corpus=corpus
        )
    
    # works on friends table
    def select_friends(self, count=False, approved=True, order="ASC", limit=CONFIG.SELECT_LIMIT, sender_id=None, recipient_id=None):
        return friends.select_friends(
            self.cur,
            count=count,
            approved=approved,
            order=order,
            limit=limit,
            sender_id=sender_id,
            recipient_id=recipient_id
        )
    
    # works on messages table
    def select_messages(self, count=False, start=None, read=None, order="DESC", limit=CONFIG.SELECT_LIMIT, message_id=None, sender_id=None, recipient_id=None):
        return messages.select_messages(
            self.cur,
            count=count,
            start=start,
            read=None,
            order=order,
            limit=limit,
            message_id=message_id,
            sender_id=sender_id,
            recipient_id=recipient_id
        )
    
    def select_user_conversations(self, user_id, count=False, order="DESC", limit=CONFIG.SELECT_LIMIT):
        return messages.select_user_conversations(
            self.cur,
            user_id=user_id,
            count=count,
            order=order,
            limit=limit
        )
    
    def insert_message(self, sender_id, recipient_id, corpus):
        messages.insert_message(
            self.cur,
            sender_id=sender_id,
            recipient_id=recipient_id,
            corpus=corpus
        )