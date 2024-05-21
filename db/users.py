from time import time


def select_users(cur, count, online, start, visible, order, limit, email, user_id):
    select = "COUNT(*)" if count else "*"

    params = [
        start,
        visible,
    ]
    if email:
        params.append(email)
    if user_id:
        params.append(user_id)
    params.append(limit)

    cur.execute(f"""
        SELECT {select}
        FROM users
        WHERE last_seen > {"NOW() - INTERVAL 5 MINUTE" if online else 0}
        AND user_id > ?
        AND visible = ?
        {"AND email = ?" if email else ""}
        {"AND user_id = ?" if user_id else ""}
        ORDER BY user_id {order}
        LIMIT ?;
    """, params)

    return cur.fetchone()["COUNT(*)"] if count else cur.fetchall()
    
def insert_user(cur, email, username, password):
    cur.execute("""
        INSERT INTO users (email, username, password)
        VALUES (?, ?, ?);
    """, [
            email,
            username, 
            password
        ]
    )
