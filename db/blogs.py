def select_blogs(cur, count, visible, order, limit, blog_id, author_id):
    params = [visible, visible]
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

def search_blogs(cur, search_term):
    cur.execute("""
        SELECT *
        FROM blogs
        LEFT JOIN users
        ON blogs.author_id = users.user_id
        WHERE MATCH(blogs.title, blogs.corpus) AGAINST (?)
        AND blogs.visible = 1;
    """, [search_term])

    return cur.fetchall()

def insert_blog(cur, author_id, title, corpus):
    cur.execute("""
        INSERT INTO blogs (author_id, title, corpus)
        VALUES (?, ?, ?);
    """, [author_id, title, corpus])