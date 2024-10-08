from mariadb import Cursor


def select_page_comments(
    cur: Cursor,
    count: bool,
    visible: bool,
    approved: bool,
    order: str,
    limit: int,
    comment_id: int | None,
    page_id: int | None,
    author_id: int | None,
) -> list:
    params: list = [visible, visible, approved]
    if comment_id:
        params.append(comment_id)
    if page_id:
        params.append(page_id)
    if author_id:
        params.append(author_id)
    params.append(limit)

    cur.execute(
        f"""
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
    """,
        params,
    )

    return cur.fetchall()


def insert_page_comment(cur: Cursor, page_id: int, author_id: int, corpus: str) -> None:
    cur.execute(
        """
        INSERT INTO page_comments (page_id, author_id, corpus)
        VALUES (?, ?, ?);
    """,
        [page_id, author_id, corpus],
    )


def delete_page_comment(cur: Cursor, comment_id: int, soft: bool, limit: int) -> None:
    if soft:
        cur.execute(
            """
            UPDATE page_comments
            SET visible = FALSE
            WHERE comment_id = ?
            LIMIT ?;
        """,
            [comment_id, limit],
        )
    else:
        cur.execute(
            """
            DELETE FROM page_comments
            WHERE comment_id = ?
            LIMIT ?;
        """,
            [comment_id, limit],
        )
