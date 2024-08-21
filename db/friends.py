def select_friends(cur, count, approved, order, limit, sender_id, recipient_id):
    params = []
    if approved is not None:
        params.append(approved)
    if sender_id:
        params.append(sender_id)
    if recipient_id:
        params.append(recipient_id)
    params.append(limit)

    if sender_id and not recipient_id:
        cur.execute(f"""
            SELECT {"COUNT(*)" if count else "*"}
            FROM friends 
            LEFT JOIN users ON users.user_id = friends.recipient_id
            {"WHERE friends.approved = ?" if approved is not None else ""}
            {"AND " if approved is not None else "WHERE "}{"friends.sender_id = ?" if sender_id else ""}
            ORDER BY friends.friend_id {order}
            LIMIT ?;
        """, params)
    elif recipient_id and not sender_id:
        cur.execute(f"""
            SELECT {"COUNT(*)" if count else "*"}
            FROM friends 
            LEFT JOIN users ON users.user_id = friends.sender_id
            {"WHERE friends.approved = ?" if approved is not None else ""}
            {"AND " if approved is not None else "WHERE "}{"friends.recipient_id = ?" if recipient_id else ""}
            ORDER BY friends.friend_id {order}
            LIMIT ?;
        """, params)
    else:
        cur.execute(f"""
            SELECT {"COUNT(*)" if count else "*"}
            FROM friends 
            {"WHERE friends.approved = ?" if approved is not None else ""}
            {"AND" if approved is not None else "WHERE"} friends.sender_id = ?
            AND friends.recipient_id = ?
            ORDER BY friends.friend_id {order}
            LIMIT ?;
        """, params)

    return cur.fetchall()

def insert_friend(cur, sender_id, recipient_id, approved):
    cur.execute("""
        INSERT INTO friends (sender_id, recipient_id, approved)
        VALUES (?, ?, ?);
    """, [sender_id, recipient_id, approved])

def update_friend(cur, sender_id, recipient_id, approved):
    cur.execute("""
        UPDATE friends
        SET approved = ?
        WHERE sender_id = ?
        AND recipient_id = ?
    """, [approved, sender_id, recipient_id])