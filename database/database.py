"""
Database connection module.

This module is responsible for creating and returning
a SQLite database connection.
"""

import sqlite3

DATABASE_NAME = "chatbot.db"


def get_connection() -> sqlite3.Connection:
    """
    Create and return a SQLite database connection.

    Returns:
        sqlite3.Connection: SQLite connection object.
    """
    conn = sqlite3.connect(DATABASE_NAME)

    # Allows accessing columns by name instead of index
    conn.row_factory = sqlite3.Row

    return conn