from mariadb import Cursor


def select_messages(
    cur: Cursor,
    count: bool,
    start: int | None,
    read: bool | None,
    order: str,
    limit: int,
    message_id: int | None,
    sender_id: int | None,
    recipient_id: int | None,
) -> list:
    params: list = []
    if start:
        params.append(start)
    if read is not None:
        params.append(read)
    if message_id:
        params.append(message_id)
    if sender_id:
        params.append(sender_id)
    if recipient_id:
        params.append(recipient_id)
    params.append(limit)

    cur.execute(
        f"""
        SELECT {"COUNT(*)" if count else "*"}
        FROM messages
        LEFT JOIN users ON messages.sender_id = users.user_id
        WHERE 1 = 1
        {"AND messages.message_id > ?" if start else ""}
        {"AND messages.read = ?" if read is not None else ""}
        {"AND messages.message_id = ?" if message_id else ""}
        {"AND messages.sender_id = ?" if sender_id else ""}
        {"AND messages.recipient_id = ?" if recipient_id else ""}
        ORDER BY messages.message_id {order}
        LIMIT ?;
    """,
        params,
    )

    return cur.fetchall()


def select_user_conversations(
    cur: Cursor, user_id: int, count: bool, order: str, limit: int
) -> list:
    cur.execute(
        """
        SELECT DISTINCT sender_id, recipient_id
        FROM messages
        WHERE sender_id = ?
        OR recipient_id = ?
    """,
        [user_id, user_id],
    )

    return cur.fetchall()


def insert_message(cur: Cursor, sender_id: int, recipient_id: int, corpus: str) -> None:
    cur.execute(
        """
        INSERT INTO messages (sender_id, recipient_id, corpus)
        VALUES (?, ?, ?);
    """,
        [sender_id, recipient_id, corpus],
    )
