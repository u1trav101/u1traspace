from mariadb import Connection
import db.users as users
import db.page_comments as page_comments
import db.blogs as blogs
import db.blog_comments as blog_comments
import db.friends as friends
import db.messages as messages
from config import CONFIG


class _Query():
    def __init__(self, conn:Connection) -> None:
        self.conn = conn
        self.cur = conn.cursor(dictionary=True)

    def __del__(self) -> None:
        self.conn.commit()
        self.conn.close()
    
    # works on users table
    def select_users(
        self, 
        count: bool = False, 
        online: bool = False, 
        start: int = 0, 
        visible: bool = True, 
        order_by: str = "user_id", 
        order: str = "DESC", 
        limit: int = CONFIG.SELECT_LIMIT, 
        email: str | None = None, 
        user_id: int | None = None
    ) -> list | int:

        return users.select_users(
            self.cur, 
            count=count, 
            online=online, 
            start=start, 
            visible=visible,
            order_by=order_by,
            order=order,
            limit=limit,
            email=email,
            user_id=user_id
        )
    
    def search_users(self, search_term:str) -> list:
        return users.search_users(
            self.cur,
            search_term=search_term
        )
    
    def insert_user(self, email:str, username:str, password:str) -> None:
        users.insert_user(
            self.cur,
            email=email, 
            username=username, 
            password=password
        )
    
    def update_user(
        self,
        user_id: int,
        about: str | None = None,
        layout: str | None = None,
        private: bool | None = None
    ) -> None:

        users.update_user(
            self.cur,
            user_id=user_id,
            about=about,
            layout=layout,
            private=private
        )
    
    def update_last_seen(self, user_id:int) -> None:
        self.cur.callproc("update_last_seen", [user_id])
    
    def increase_page_views(self, user_id:int) -> None:
        self.cur.callproc("increase_page_views", [user_id])
    
    # works on page_comments table
    def select_page_comments(
        self,
        count: bool = False,
        visible: bool = True,
        approved: bool = True,
        order: str = "DESC",
        limit: int = CONFIG.SELECT_LIMIT,
        comment_id: int | None = None,
        page_id: int | None = None,
        author_id: int | None =None
    ) -> list:

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
    
    def insert_page_comment(self, page_id:int, author_id:int, corpus:str) -> None:
        page_comments.insert_page_comment(
            self.cur,
            page_id=page_id,
            author_id=author_id,
            corpus=corpus
        )

    # works on blogs table
    def select_blogs(
        self,
        count: bool = False,
        visible: bool = True,
        order: str = "DESC",
        limit: int = CONFIG.SELECT_LIMIT,
        blog_id: int | None = None,
        author_id: int | None = None
    ) -> list:

        return blogs.select_blogs(
            self.cur,
            count=count,
            visible=visible,
            order=order,
            limit=limit,
            blog_id=blog_id,
            author_id=author_id
        )
    
    def search_blogs(self, search_term:str) -> list:
        return blogs.search_blogs(
            self.cur,
            search_term=search_term
        )
    
    def insert_blog(self, author_id:int, title:str, corpus:str) -> None:
        blogs.insert_blog(
            self.cur,
            author_id=author_id,
            title=title,
            corpus=corpus
        )
    
    # works on blog_comments table
    def select_blog_comments(
        self,
        count: bool = False,
        visible: bool = True,
        approved: bool = True,
        order: str = "DESC",
        limit: int = CONFIG.SELECT_LIMIT,
        comment_id: int | None = None,
        blog_id: int | None = None,
        author_id: int | None = None
    ) -> list:

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
    
    def select_pending_blog_comments(
        self,
        count: bool = False,
        visible: bool = True,
        order: str = "DESC",
        limit: int = CONFIG.SELECT_LIMIT,
        blog_id: int | None = None,
        author_id: int | None =None
    ) -> list:

        return blog_comments.select_pending_blog_comments(
            self.cur,
            count=count,
            visible=visible,
            order=order,
            limit=limit,
            blog_id=blog_id,
            author_id=author_id
        )
    
    def insert_blog_comment(self, blog_id:int, author_id:int, corpus:str) -> None:
        blog_comments.insert_blog_comment(
            self.cur,
            blog_id=blog_id,
            author_id=author_id,
            corpus=corpus
        )
    
    # works on friends table
    def select_friends(
        self,
        count: bool = False,
        approved: bool | None = True,
        order: str = "ASC",
        limit: int = CONFIG.SELECT_LIMIT,
        sender_id: int | None = None,
        recipient_id: int | None = None
        ) -> list:

        return friends.select_friends(
            self.cur,
            count=count,
            approved=approved,
            order=order,
            limit=limit,
            sender_id=sender_id,
            recipient_id=recipient_id
        )
    
    def insert_friend(self, sender_id:int, recipient_id:int, approved:bool=False) -> None:
        friends.insert_friend(
            self.cur,
            sender_id=sender_id,
            recipient_id=recipient_id,
            approved=approved
        )
    
    def update_friend(self, sender_id:int, recipient_id:int, approved:bool) -> None:
        friends.update_friend(
            self.cur,
            sender_id=sender_id,
            recipient_id=recipient_id,
            approved=approved
        )
    
    # works on messages table
    def select_messages(
        self,
        count: bool = False,
        start: int | None = None,
        read: bool | None = None,
        order: str = "DESC",
        limit: int = CONFIG.SELECT_LIMIT,
        message_id: int | None = None,
        sender_id: int | None = None,
        recipient_id: int | None =None
        ) -> list:

        return messages.select_messages(
            self.cur,
            count=count,
            start=start,
            read=read,
            order=order,
            limit=limit,
            message_id=message_id,
            sender_id=sender_id,
            recipient_id=recipient_id
        )
    
    def select_user_conversations(self, user_id:int, count:bool=False, order:str="DESC", limit:int=CONFIG.SELECT_LIMIT) -> list:
        return messages.select_user_conversations(
            self.cur,
            user_id=user_id,
            count=count,
            order=order,
            limit=limit
        )
    
    def insert_message(self, sender_id:int, recipient_id:int, corpus:str):
        messages.insert_message(
            self.cur,
            sender_id=sender_id,
            recipient_id=recipient_id,
            corpus=corpus
        )