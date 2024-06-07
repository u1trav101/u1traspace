def select_users(cur, count, online, start, visible, order_by, order, limit, email, user_id):
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
        ORDER BY {order_by} {order}
        LIMIT ?;
    """, params)

    return cur.fetchone()["COUNT(*)"] if count else cur.fetchall()

def search_users(cur, search_term):
    cur.execute("""
        SELECT *
        FROM users
        WHERE MATCH(username) AGAINST (?)
        AND visible = 1;
    """, [search_term])

    return cur.fetchall()
    
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

def update_user(cur, user_id, about, layout, private):
    if about:
        cur.execute("""
            UPDATE users
            SET about = ?
            WHERE user_id = ?
            LIMIT 1;
        """, [about, user_id])
    else:
        print("nulling")
        cur.execute("""
            UPDATE users
            SET about = NULL
            WHERE user_id = ?
            LIMIT 1;
        """, [user_id])
    
    if layout:
        cur.execute("""
            UPDATE users
            SET layout = ?
            WHERE user_id = ?
            LIMIT 1;
        """, [layout, user_id])
    
    if private is not None:
        cur.execute("""
            UPDATE users
            SET private = ?
            WHERE user_id = ?
            LIMIT 1;
        """, [private, user_id])