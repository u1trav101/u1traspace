from time import time
from random import randint


class _Query():
    def __init__(self, conn):
        self.conn = conn
        self.cur = conn.cursor(dictionary=True)

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def get_user_by_id(self, id):
        self.cur.execute("""
            SELECT *
            FROM users
            WHERE id = ?
            LIMIT 1;
            """, [id])

        return self.cur.fetchone()

    def get_id_by_username(self, username):
        self.cur.execute("""
            SELECT id
            FROM users
            WHERE username = ?
            LIMIT 1;
        """, [username])

        try:
            return int(self.cur.fetchone()[0])
        except KeyError:
            return None

    def get_number_of_users(self, filter_online):
        if filter_online:
            self.cur.execute("""
                SELECT COUNT(*)
                FROM users
                LEFT JOIN
                    userinfo ON users.id = userinfo.id
                WHERE
                    users.id NOT IN (SELECT banid from slops)
                    AND userinfo.lastseen > ?
            """, [round(time()) - 300])
        else:
            self.cur.execute("""
                SELECT COUNT(*)
                FROM users
                WHERE id NOT IN (SELECT banid from slops);
            """)

        return int(self.cur.fetchone()["COUNT(*)"])

    def get_list_of_users(self, min, filter_online):
        # Selects user accounts that haven't been banned
        # Banned users are stored in 'slops' table
        if filter_online:
            self.cur.execute("""
                SELECT
                    users.id,
                    users.username,
                    userinfo.lastseen,
                    userinfo.pagecount
                FROM users left JOIN userinfo ON users.id = userinfo.id
                WHERE
                    users.id NOT IN (SELECT banid from slops)
                    AND userinfo.lastseen > ?
                ORDER BY users.id ASC
                LIMIT ?, 15;
            """, [round(time()) - 300, min])
        else:
            self.cur.execute("""
                SELECT
                    users.id,
                    users.username,
                    userinfo.lastseen,
                    userinfo.pagecount
                FROM users left JOIN userinfo ON users.id = userinfo.id
                WHERE users.id NOT IN (SELECT banid from slops)
                ORDER BY users.id ASC
                LIMIT ?, 15;
            """, [min])

        return self.cur.fetchall()

    def add_user(self, username, password):
        self.cur.execute("""
            SELECT COUNT(*)
            FROM users
        """)
        user_id = int(self.cur.fetchone()["COUNT(*)"])

        self.cur.execute("""
            INSERT INTO users (id, username, password)
            VALUES (?, ?, ?);
        """, [user_id, username, password])

        self.cur.execute("""
            INSERT INTO userinfo (id, age, about, interface, lastseen, joindate, pagecount)
            VALUES (?, 0, 'new', 'default', 0, ?, 0)
        """, [user_id, round(time())])

        return user_id

    def get_user_profile(self, id):
        self.cur.execute("""
            SELECT
                userinfo.*,
                users.username
            FROM userinfo LEFT JOIN users ON userinfo.id = users.id
            WHERE userinfo.id = ?
            AND users.id NOT IN (SELECT banid FROM slops)
            LIMIT 1;
        """, [id])

        return self.cur.fetchone()

    def get_random_user_profile(self):
        self.cur.execute("""
            SELECT id
            FROM users
            WHERE id NOT IN (SELECT banid FROM slops);
        """)

        users = self.cur.fetchall()

        return users[randint(0, len(users) - 1)]["id"]

    def get_user_comment(self, comment_id, page_id):
        self.cur.execute("""
            SELECT
                corpus,
                date
            FROM user_comments
            WHERE id = ?
            AND pageid = ?
            LIMIT 1;
        """, [comment_id, page_id])

        return self.cur.fetchone()

    def get_user_comments(self, page_id):
        self.cur.execute("""
            SELECT
                user_comments.id,
                user_comments.authorid,
                user_comments.corpus,
                user_comments.date,
                users.username
            FROM user_comments LEFT JOIN users ON user_comments.authorid = users.id
            WHERE user_comments.state = 1
            AND user_comments.pageid = ?
            ORDER BY user_comments.id DESC;
        """, [page_id])

        return self.cur.fetchall()

    def get_all_user_blogposts(self, user_id):
        self.cur.execute("""
            SELECT
                id,
                title,
                corpus,
                date
            FROM blogs
            WHERE authorid = ?
            AND state = 1
            ORDER BY ID DESC;
        """, [user_id])

        return self.cur.fetchall()
    
    def get_all_friend_blogposts(self, user_id, limit=999999999999):
        self.cur.execute("""
            SELECT
                blogs.authorid,
                blogs.id,
                blogs.title,
                blogs.date,
                users.username
            FROM blogs
            LEFT JOIN users
                ON users.id = blogs.authorid
            WHERE blogs.state = 1
            ORDER BY blogs.date DESC 
            LIMIT ?; 
        """)

    def get_all_blogposts(self, limit=999999999999):
        self.cur.execute("""
            SELECT
                blogs.authorid,
                blogs.id,
                blogs.title,
                blogs.date,
                users.username
            FROM blogs
            LEFT JOIN users
                ON users.id = blogs.authorid
            WHERE blogs.state = 1
            ORDER BY blogs.date DESC 
            LIMIT ?;
        """, [limit])

        return self.cur.fetchall()

    def get_blogpost(self, user_id, post_id):
        self.cur.execute("""
            SELECT
                id,
                title,
                corpus,
                date
            FROM blogs
            WHERE id = ?
            AND authorid = ?
            AND state = 1
            LIMIT 1;
        """, [post_id, user_id])

        return self.cur.fetchone()

    def get_blogpost_comment(self, author_id, comment_id, blog_id, page_id):
        self.cur.execute("""
            SELECT
                corpus,
                date
            FROM blog_comments
            WHERE id = ?
            AND blogid = ?
            AND authorid = ?
            AND pageid = ?
            LIMIT 1;
        """, [comment_id, blog_id, author_id, page_id])

        return self.cur.fetchone()

    def get_blogpost_comments(self, user_id, post_id):
        self.cur.execute("""
            SELECT
                blog_comments.id,
                blog_comments.authorid,
                blog_comments.corpus,
                blog_comments.date,
                users.username
            FROM blog_comments LEFT JOIN users ON blog_comments.authorid = users.id
            WHERE blog_comments.state = 1
            AND blog_comments.pageid = ?
            AND blog_comments.blogid = ?
            ORDER BY blog_comments.id DESC;
        """, [user_id, post_id])

        return self.cur.fetchall()

    def blogpost_comment_action(self, action, comment_id, author_id, page_id, blog_id):
        self.cur.execute("""
            UPDATE blog_comments
            SET state = ?
            WHERE id = ?
            AND authorid = ?
            AND pageid = ?
            AND blogid = ?
            LIMIT 1;
        """, [action, comment_id, author_id, page_id, blog_id])

    def add_blogpost(self, user_id, title, corpus):
        self.cur.execute("""
            SELECT id
            FROM blogs
            WHERE authorid = ?
            ORDER BY id DESC
            LIMIT 1;
        """, [user_id])

        blog_id = 0
        try:
            blog_id = self.cur.fetchone()["id"] + 1
        except TypeError:
            pass

        self.cur.execute("""
            INSERT INTO blogs
            VALUES (?, ?, ?, ?, ?, 1)
        """, [blog_id, user_id, title, corpus, round(time())])

        return blog_id
    
    def delete_blogpost(self, author_id, blog_id):
        self.cur.execute("""
            UPDATE blogs
            SET state = 0
            WHERE authorid = ?
            AND id = ?
            LIMIT 1;
        """, [author_id, blog_id])

    def get_number_of_messages(self):
        self.cur.execute("""
            SELECT messageid
            FROM messages
            ORDER BY messageid DESC
            LIMIT 1;
        """)

        return int(self.cur.fetchone()[0])

    def add_message(self, sender_id, recipient_id, corpus):
        self.cur.execute("""
            INSERT INTO messages (senderid, recipientid, corpus, date)
            VALUES (?, ?, ?, ?);
        """, [sender_id, recipient_id, corpus, round(time())])

        self.cur.execute("""
            INSERT INTO notifications (userid, actionuserid, type)
            VALUES (?, ?, 'unseen_message');
        """, [recipient_id, sender_id])

    def clear_message_notifications(self, user_id, recipient_id):
        self.cur.execute("""
            DELETE FROM notifications
            WHERE actionuserid = ?
            AND userid = ?
            AND type = 'unseen_message';
        """, [recipient_id, user_id])

    def get_message_senders(self, recipient_id):
        self.cur.execute("""
            SELECT
                users.id,
                users.username
            FROM messages LEFT JOIN users ON messages.senderid = users.id
            WHERE messages.recipientid = ?
            OR messages.senderid = ?
            ORDER BY messages.messageid ASC;
        """, [recipient_id, recipient_id])

        return self.cur.fetchall()

    def get_all_user_messages(self, recipient_id, sender_id):
        self.cur.execute("""
            SELECT
                messages.messageid,
                messages.senderid,
                messages.corpus,
                messages.date,
                users.username
            FROM messages
            LEFT JOIN users
                ON messages.senderid = users.id
            WHERE (messages.recipientid = ? AND messages.senderid = ?)
            OR (messages.recipientid = ? AND messages.senderid = ?)
            ORDER BY messages.messageid DESC;
        """, [recipient_id, sender_id, sender_id, recipient_id])

        return self.cur.fetchall()

    def get_user_conversations(self, user_id):
        self.cur.execute("""
            SELECT DISTINCT
                senderid,
                recipientid
            FROM messages
            WHERE senderid = ?
            OR recipientid = ?;
        """, [user_id, user_id])

        return self.cur.fetchall()
    
    def get_last_message_in_conversation(self, sender_id, recipient_id):
        self.cur.execute("""
            SELECT
                senderid,
                corpus,
                date
            FROM messages
            WHERE (senderid = ? AND recipientid = ?)
            OR (recipientid = ? AND senderid = ?)
            ORDER BY messageid DESC
            LIMIT 1;
        """, [sender_id, recipient_id, sender_id, recipient_id])

        return self.cur.fetchone()

    def poll_incoming_messages(self, sender_id, recipient_id, last_message_id):
        self.cur.execute("""
            SELECT
                messages.messageid,
                messages.senderid,
                messages.corpus,
                messages.date,
                users.username
            FROM messages
            LEFT JOIN users
                ON messages.senderid = users.id
            WHERE ((messages.recipientid = ? AND messages.senderid = ?)
            OR (messages.recipientid = ? AND messages.senderid = ?))
            AND messages.messageid > ?
            ORDER BY messages.date ASC;
        """, [recipient_id, sender_id, sender_id, recipient_id, last_message_id])

        return self.cur.fetchall()

    def search_usernames(self, search_text):
        self.cur.execute("""
            SELECT
                id,
                username
            FROM users
            WHERE MATCH(username) AGAINST (?);
        """, [search_text])

        return self.cur.fetchall()

    def search_blogs(self, search_text):
        self.cur.execute("""
            SELECT
                blogs.id,
                blogs.authorid,
                blogs.title,
                blogs.corpus,
                blogs.date,
                users.username
            FROM blogs
            LEFT JOIN users
            ON blogs.authorid = users.id
            WHERE MATCH(title, corpus) AGAINST (?)
            AND blogs.state = 1;
        """, [search_text.replace(" ", ",")])

        return self.cur.fetchall()

    def update_last_seen(self, user_id):
        self.cur.execute("""
            UPDATE userinfo
            SET lastseen = ?
            WHERE id = ?
            LIMIT 1;
        """, [round(time()), user_id])

    def update_page_views(self, user_id):
        self.cur.execute("""
            UPDATE userinfo
            SET pagecount = pagecount + 1
            WHERE id = ?
            LIMIT 1;
        """, [user_id])

    def add_profile_comment(self, author_id, profile_id, corpus):
        # gets the id of the comment
        self.cur.execute("""
            SELECT id
            FROM user_comments
            WHERE pageid = ?
            ORDER BY id DESC
            LIMIT 1;
        """, [profile_id])

        comment_id = 0
        try:
            comment_id = int(self.cur.fetchone()["id"]) + 1
        except TypeError:
            pass

        # determines whether or not the profile is private
        self.cur.execute("""
            SELECT private
            FROM userinfo
            WHERE id = ?
            LIMIT 1;
        """, [profile_id])

        state = 1
        if int.from_bytes(self.cur.fetchone()["private"], "big") == 1:
            self.cur.execute("""
                SELECT friend
                FROM friends
                WHERE id = ?
                AND friend = ?
                AND state = 1
                LIMIT 1;
            """, [profile_id, author_id])

            if not self.cur.fetchone():
                state = 0

        # adds the blog comment
        self.cur.execute("""
            INSERT INTO user_comments
            VALUES (?, ?, ?, ?, ?, ?);
        """, [comment_id, author_id, profile_id, corpus, round(time()), state])

        # adds a notification for the comment recipient
        if author_id != profile_id:
            self.cur.execute("""
                INSERT INTO
                    notifications (userid, actionuserid, actioncommentid, type)
                VALUES (?, ?, ?, 'profile_comment_approval')
            """, [profile_id, author_id, comment_id])

    def user_comment_action(self, action, comment_id, page_id):
        self.cur.execute("""
            UPDATE user_comments
            SET state = ?
            WHERE id = ?
            AND pageid = ?
            LIMIT 1;
        """, [action, comment_id, page_id])

    def get_user_comment_author(self, page_id, comment_id):
        self.cur.execute("""
            SELECT authorid
            FROM user_comments
            WHERE id = ?
            AND pageid = ?
            LIMIT 1;
        """, [comment_id, page_id])

        return self.cur.fetchone()["authorid"]

    def delete_user_comment(self, page_id, comment_id):
        self.cur.execute("""
            UPDATE user_comments
            SET state = 0
            WHERE id = ?
            AND pageid = ?;
        """, [comment_id, page_id])

    def add_blog_comment(self, author_id, page_id, blog_id, corpus):
        self.cur.execute("""
            SELECT id
            FROM blog_comments
            WHERE pageid = ?
            AND blogid = ?
            ORDER BY id DESC
            LIMIT 1;
        """, [page_id, blog_id])

        comment_id = 0
        try:
            comment_id = int(self.cur.fetchone()["id"]) + 1
        except TypeError:
            pass

        self.cur.execute("""
            SELECT private
            FROM userinfo
            WHERE id = ?
            LIMIT 1;
        """, [page_id])

        state = 1
        if int.from_bytes(self.cur.fetchone()["private"], "big") == 1:
            self.cur.execute("""
                SELECT friend
                FROM friends
                WHERE id = ?
                AND friend = ?
                AND state = 1
                LIMIT 1;
            """, [page_id, author_id])

            if not self.cur.fetchone():
                state = 0

        self.cur.execute("""
            INSERT INTO blog_comments
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, [comment_id, author_id, page_id, blog_id, corpus, round(time()), state])

        if author_id != page_id:
            self.cur.execute("""
                INSERT INTO
                notifications (userid, actionuserid, actionpostid, actioncommentid, type)
                VALUES (?, ?, ?, ?, 'blog_comment_approval')
            """, [page_id, author_id, blog_id, comment_id])

    def get_blog_comment_author(self, page_id, blog_id, comment_id):
        self.cur.execute("""
            SELECT authorid
            FROM blog_comments
            WHERE pageid = ?
            AND blogid = ?
            AND id = ?
            LIMIT 1;
        """, [page_id, blog_id, comment_id])

        return self.cur.fetchone()["authorid"]

    def delete_blog_comment(self, blog_id, comment_id):
        self.cur.execute("""
            UPDATE blog_comments
            SET state = 0
            WHERE id = ?
            AND blogid = ?;
        """, [comment_id, blog_id])

    def get_user_friends(self, user_id):
        self.cur.execute("""
            SELECT
                friends.friend,
                users.username
            FROM friends LEFT JOIN users ON friends.friend = users.id
            WHERE friends.state = 1
            AND friends.id = ?
            ORDER BY users.username;
        """, [user_id])

        return self.cur.fetchall()

    def add_friend_request(self, user_id, friend_id):
        self.cur.execute("""
            SELECT state
            FROM friends
            WHERE id = ?
            AND friend = ?
            LIMIT 1;
        """, [user_id, friend_id])

        if not self.cur.fetchone():
            self.cur.execute("""
                INSERT INTO friends
                VALUES (?, ?, 0);
            """, [user_id, friend_id])

            return True

        return False

    def friend_approve_action(self, user_id, friend_id):
        self.cur.execute("""
            UPDATE friends
            SET state = 1
            WHERE id = ?
            AND friend = ?
            LIMIT 1;
        """, [friend_id, user_id])

        self.cur.execute("""
            INSERT INTO friends
            VALUES (?, ?, 1)
        """, [user_id, friend_id])

    def friend_reject_action(self, user_id, friend_id):
        self.cur.execute("""
            DELETE FROM friends
            WHERE id = ?
            AND friend = ?
            LIMIT 1;
        """, [friend_id, user_id])

    def update_user_preferences(self, user_id, bio, interface, privacy):
        self.cur.execute("""
            UPDATE userinfo
            SET
                about = ?,
                interface = ?,
                private = ?
            WHERE id = ?;
        """, [bio, interface, privacy, user_id])

    def get_interface_and_privacy(self, user_id):
        self.cur.execute("""
            SELECT interface, private
            FROM userinfo
            WHERE id = ?
            LIMIT 1;
        """, [user_id])

        return self.cur.fetchone()

    def add_friend_notification(self, user_id, action_user_id):
        self.cur.execute("""
            INSERT INTO
            notifications (userid, actionuserid, type)
            VALUES (?, ?, 'friend_request_approval');
        """, [user_id, action_user_id])

    def get_user_notification_types(self, user_id):
        self.cur.execute("""
            SELECT type
            FROM notifications
            WHERE userid = ?;
        """, [user_id])

        return self.cur.fetchall()

    def get_user_notification(self, notification_id):
        self.cur.execute("""
            SELECT *
            FROM notifications
            WHERE id = ?
            LIMIT 1;
        """, [notification_id])

        return self.cur.fetchone()

    def get_user_notifications(self, user_id):
        self.cur.execute("""
            SELECT
                notifications.*,
                users.username
            FROM notifications
            LEFT JOIN users ON notifications.actionuserid = users.id
            WHERE notifications.userid = ?;
        """, [user_id])

        return self.cur.fetchall()

    def delete_user_notification(self, notification_id):
        self.cur.execute("""
            DELETE
            FROM notifications
            WHERE id = ?
        """, [notification_id])
