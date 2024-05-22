def select_blog_comments(cur, count, visible, approved, order, limit, comment_id, blog_id, author_id):
    params = [visible, approved]
    if comment_id:
        params.append(comment_id)
    if blog_id:
        params.append(blog_id)
    if author_id:
        params.append(author_id)
    params.append(limit)

    cur.execute(f"""
        SELECT {"COUNT(*)" if count else "*"}
        FROM blog_comments
        LEFT JOIN users ON blog_comments.author_id = users.user_id
        WHERE blog_comments.visible = ?
        AND blog_comments.approved = ?
        {"AND blog_comments.comment_id = ?" if comment_id else ""}
        {"AND blog_comments.blog_id = ?" if blog_id else ""}
        {"AND blog_comments.author_id = ?" if author_id else ""}
        ORDER BY blog_comments.comment_id {order}
        LIMIT ?;
    """, params)

    return cur.fetchall()

def select_pending_blog_comments(cur, count, visible, order, limit, blog_id, author_id):
    params = [visible]
    if author_id:
        params.append(author_id)
    if blog_id:
        params.append(blog_id)
    params.append(limit)

    cur.execute(f"""
        SELECT {"COUNT(*)" if count else "*"}
        FROM blog_comments
        LEFT JOIN blogs ON blog_comments.blog_id = blogs.blog_id
        LEFT JOIN users ON blogs.author_id = users.user_id
        WHERE blog_comments.visible = ?
        {"AND blogs.author_id = ?" if author_id else ""}
        {"AND blogs.blog_id = ?" if blog_id else ""}
        ORDER BY blog_comments.comment_id {order}
        LIMIT ?;
    """, params)

    return cur.fetchall()

def insert_blog_comment(cur, blog_id, author_id, corpus):
    cur.execute("""
        INSERT INTO blog_comments (blog_id, author_id, corpus)
        VALUES (?, ?, ?);
    """, [blog_id, author_id, corpus])