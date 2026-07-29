"""
Database models and CRUD operations.
"""

from database.database import get_connection


# ==========================================================
# DATABASE INITIALIZATION
# ==========================================================

def initialize_database() -> None:
    """
    Create database tables if they don't already exist.
    """

    conn = get_connection()
    cursor = conn.cursor()

    # -------------------------------
    # Chats Table
    # -------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            thread_id TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # -------------------------------
    # Messages Table
    # -------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(chat_id) REFERENCES chats(id)
        )
    """)

    conn.commit()
    conn.close()


# ==========================================================
# CHAT CRUD
# ==========================================================

def create_chat(title: str, thread_id: str) -> None:
    """
    Create a new chat.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO chats(title, thread_id)
        VALUES (?, ?)
        """,
        (title, thread_id),
    )

    conn.commit()
    conn.close()


def get_all_chats():
    """
    Return all chats ordered by newest first.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM chats
        ORDER BY created_at DESC
    """)

    chats = cursor.fetchall()

    conn.close()

    return chats


def get_chat_by_thread(thread_id: str):
    """
    Return a single chat using thread id.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM chats
        WHERE thread_id = ?
        """,
        (thread_id,),
    )

    chat = cursor.fetchone()

    conn.close()

    return chat


def delete_chat(thread_id: str) -> None:
    """
    Delete a chat using thread id.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM chats
        WHERE thread_id = ?
        """,
        (thread_id,),
    )

    conn.commit()
    conn.close()


# ==========================================================
# MESSAGE CRUD
# ==========================================================

def save_message(chat_id: int, role: str, content: str) -> None:
    """
    Save a chat message.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO messages(chat_id, role, content)
        VALUES (?, ?, ?)
        """,
        (chat_id, role, content),
    )

    conn.commit()
    conn.close()


def get_messages(chat_id: int):
    """
    Return all messages for a chat.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM messages
        WHERE chat_id = ?
        ORDER BY created_at
        """,
        (chat_id,),
    )

    messages = cursor.fetchall()

    conn.close()

    return messages


def delete_messages(chat_id: int) -> None:
    """
    Delete all messages belonging to a chat.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM messages
        WHERE chat_id = ?
        """,
        (chat_id,),
    )

    conn.commit()
    conn.close()
    
def update_chat_title(thread_id: str, title: str) -> None:
        """
        Update chat title.
        """

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE chats
            SET title = ?
            WHERE thread_id = ?
            """,
            (
                title,
                thread_id,
            ),
        )

        conn.commit()
        conn.close()