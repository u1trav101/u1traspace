def select_page_comments(cur, count, visible, approved, order, limit, comment_id, page_id, author_id):
    params = [visible, visible, approved]
    if comment_id:
        params.append(comment_id)
    if page_id:
        params.append(page_id)
    if author_id:
        params.append(author_id)
    params.append(limit)

    cur.execute(f"""
        SELECT {"COUNT(*)" if count else "*"}
        FROM page_comments
        LEFT JOIN users ON page_comments.author_id = users.user_id
        WHERE page_comments.visible = ?
        AND users.visible = ?
        AND page_comments.approved = ?
        {"AND page_comments.comment_id = ?" if comment_id else ""}
        {"AND page_comments.page_id = ?" if page_id else ""}
        {"AND page_comments.author_id = ?" if author_id else ""}
        ORDER BY page_comments.comment_id {order}
        LIMIT ?;
    """, params)

    return cur.fetchall()

def insert_page_comment(cur, page_id, author_id, corpus):
    cur.execute("""
        INSERT INTO page_comments (page_id, author_id, corpus)
        VALUES (?, ?, ?);
    """, [page_id, author_id, corpus])