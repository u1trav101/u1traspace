from mariadb import Cursor


def select_blogs(cur:Cursor, count:int, visible:bool, order:str, limit:int, blog_id:int|None, author_id:int|None) -> list:
    params: list = [visible, visible]
    if blog_id:
        params.append(blog_id)
    if author_id:
        params.append(author_id)
    params.append(limit)

    cur.execute(f"""
        SELECT {"COUNT(*)" if count else "*"} 
        FROM blogs
        LEFT JOIN users ON blogs.author_id = users.user_id
        WHERE blogs.visible = ?
        AND users.visible = ?
        {"AND blogs.blog_id = ?" if blog_id else ""}
        {"AND blogs.author_id = ?" if author_id else ""}
        ORDER BY blogs.blog_id {order}
        LIMIT ?;
    """, params)

    return cur.fetchall()

def search_blogs(cur:Cursor, search_term:str) -> list:
    cur.execute("""
        SELECT *
        FROM blogs
        LEFT JOIN users
        ON blogs.author_id = users.user_id
        WHERE MATCH(blogs.title, blogs.corpus) AGAINST (?)
        AND blogs.visible = 1;
    """, [search_term])

    return cur.fetchall()

def insert_blog(cur:Cursor, author_id:int, title:str, corpus:str) -> None:
    cur.execute("""
        INSERT INTO blogs (author_id, title, corpus)
        VALUES (?, ?, ?);
    """, [author_id, title, corpus])

def delete_blog(cur:Cursor, blog_id:int, soft:bool, limit:int) -> None:
    if soft:
        cur.execute("""
            UPDATE blogs
            SET visible = FALSE
            WHERE blog_id = ?
            LIMIT ?;
        """, [blog_id, limit])
    else:
        cur.execute("""
            DELETE FROM blogs
            WHERE blog_id = ?
            LIMIT ?;
        """, [blog_id, limit])