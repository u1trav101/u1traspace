def select_friends(cur, count, approved, order, limit, sender_id, recipient_id):
    params = [approved]
    if sender_id:
        params.append(sender_id)
    if recipient_id:
        params.append(recipient_id)
    params.append(limit)

    cur.execute(f"""
        SELECT {"COUNT(*)" if count else "*"}
        FROM friends 
        LEFT JOIN users ON users.user_id = friends.recipient_id
        WHERE friends.approved = ?
        {"AND friends.sender_id = ?" if sender_id else ""}
        {"AND friends.recipient_id = ?" if recipient_id else ""}
        ORDER BY friends.relationship_id {order}
        LIMIT ?;
    """, params)

    return cur.fetchall()