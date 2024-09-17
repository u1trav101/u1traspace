from typing import Any
from mariadb import Cursor


def select_users(
    cur: Cursor,
    count: bool,
    online: bool,
    start: int,
    visible: bool,
    order_by: str,
    order: str,
    limit: int,
    random: bool,
    email: str | None,
    user_id: int | None,
    seed: int | None,
) -> list | int:
    select: str = "COUNT(*)" if count else "*"

    params: list = [visible]
    if email:
        params.append(email)
    if user_id:
        params.append(user_id)
    params.append(start)
    params.append(limit)

    cur.execute(
        f"""
        SELECT {select}
        FROM users
        WHERE last_seen > {"NOW() - INTERVAL 5 MINUTE" if online else 0}
        AND visible = ?
        {"AND email = ?" if email else ""}
        {"AND user_id = ?" if user_id else ""}
        {f"ORDER BY {order_by} {order}" if not random else ""}
        {"ORDER BY RAND()" if (random and not seed) else ""}
        {f"ORDER BY RAND({seed})" if (random and seed) else ""}
        LIMIT ?, ?;
    """,
        params,
    )

    return cur.fetchone()["COUNT(*)"] if count else cur.fetchall()


def search_users(cur: Cursor, search_term: str) -> list:
    cur.execute(
        """
        SELECT *
        FROM users
        WHERE MATCH(username) AGAINST (?)
        AND visible = 1;
    """,
        [search_term],
    )

    return cur.fetchall()


def insert_user(cur: Cursor, email: str, username: str, password: str) -> None:
    cur.execute(
        """
        INSERT INTO users (email, username, password)
        VALUES (?, ?, ?);
    """,
        [email, username, password],
    )


def update_user(
    cur: Cursor,
    user_id: int,
    about: str | None,
    layout: str | None,
    private: bool | None,
) -> None:
    if about:
        cur.execute(
            """
            UPDATE users
            SET about = ?
            WHERE user_id = ?
            LIMIT 1;
        """,
            [about, user_id],
        )
    else:
        cur.execute(
            """
            UPDATE users
            SET about = NULL
            WHERE user_id = ?
            LIMIT 1;
        """,
            [user_id],
        )

    if layout:
        cur.execute(
            """
            UPDATE users
            SET layout = ?
            WHERE user_id = ?
            LIMIT 1;
        """,
            [layout, user_id],
        )

    if private is not None:
        cur.execute(
            """
            UPDATE users
            SET private = ?
            WHERE user_id = ?
            LIMIT 1;
        """,
            [private, user_id],
        )
