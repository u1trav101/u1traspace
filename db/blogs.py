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