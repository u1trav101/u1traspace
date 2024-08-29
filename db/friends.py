from mariadb import Cursor


def select_friends(cur:Cursor, count:int, approved:bool|None, order:str, limit:int, sender_id:int|None, recipient_id:int|None) -> list:
    params: list = []
    if approved is not None:
        params.append(approved)
    if sender_id:
        params.append(sender_id)
    if recipient_id:
        params.append(recipient_id)
    params.append(limit)

    if sender_id and not recipient_id: # if only sender_id is provided then only JOIN on recipient_id
        cur.execute(f"""
            SELECT {"COUNT(*)" if count else "*"}
            FROM friends 
            LEFT JOIN users ON users.user_id = friends.recipient_id
            {"WHERE friends.approved = ?" if approved is not None else ""}
            {"AND " if approved is not None else "WHERE "}{"friends.sender_id = ?" if sender_id else ""}
            ORDER BY friends.friend_id {order}
            LIMIT ?;
        """, params)
    elif recipient_id and not sender_id: # if only recipient_id is provided then only JOIN on sender_id
        cur.execute(f"""
            SELECT {"COUNT(*)" if count else "*"}
            FROM friends 
            LEFT JOIN users ON users.user_id = friends.sender_id
            {"WHERE friends.approved = ?" if approved is not None else ""}
            {"AND " if approved is not None else "WHERE "}{"friends.recipient_id = ?" if recipient_id else ""}
            ORDER BY friends.friend_id {order}
            LIMIT ?;
        """, params)
    else: # if both sender_id and recipient_id is provided then don't JOIN on anything
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

def insert_friend(cur:Cursor, sender_id:int, recipient_id:int, approved:bool) -> None:
    cur.execute("""
        INSERT INTO friends (sender_id, recipient_id, approved)
        VALUES (?, ?, ?);
    """, [sender_id, recipient_id, approved])

def update_friend(cur:Cursor, sender_id:int, recipient_id:int, approved:bool) -> None:
    cur.execute("""
        UPDATE friends
        SET approved = ?
        WHERE sender_id = ?
        AND recipient_id = ?
    """, [approved, sender_id, recipient_id])

def delete_friend(cur:Cursor, friend_id:int) -> None:
    cur.execute("""
        DELETE FROM friends
        WHERE friend_id = ?
        LIMIT 1;
    """, [friend_id])