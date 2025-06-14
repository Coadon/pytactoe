import os
import sqlite3
import sys

from appdirs import user_data_dir

from constants import RoundResult
from record import RoundRecord


def serialize_round_result(result: RoundResult, won_on_time: bool) -> int:
    return int(result) + (16 if won_on_time else 0)


def deserialize_round_result(result) -> (int, bool):
    won_on_time = result >= 16
    return result % 16, won_on_time


# Creates a new database file if it doesn’t exist.
conn: sqlite3.Connection
cur: sqlite3.Cursor


def start():
    data_dir = user_data_dir("py-tac-toe", "fortpile")
    os.makedirs(data_dir, exist_ok=True)
    db_path = os.path.join(data_dir, "rounds.sqlite")

    print("Data directory: ", data_dir)
    print("Using DB path: ", db_path)

    global conn, cur
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Create the table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS rounds ( \
            id INTEGER PRIMARY KEY AUTOINCREMENT, \
            record TEXT NOT NULL, \
            round_result INTEGER NOT NULL, \
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP \
        )
    """)
    conn.commit()
    print("Table initialized.")


def add_round(round_record: RoundRecord):
    record_str = repr(round_record)
    cur.execute("INSERT INTO rounds (record, round_result) VALUES (?, ?)",
                (record_str,
                 serialize_round_result(
                     round_record.result,
                     round_record.won_on_time)))
    conn.commit()
    print("Round pushed to table.")


def get_all_rounds():
    cur.execute("SELECT * FROM rounds")
    return cur.fetchall()


def get_round_by_id(round_id: int):
    cur.execute("SELECT * FROM rounds WHERE id = ?", (round_id,))
    return cur.fetchone()


def get_round_range(low: int, end: int):
    cur.execute("SELECT * FROM rounds WHERE id BETWEEN ? AND ? ORDER BY id ASC", (low, end))
    return cur.fetchall()


def get_round_count() -> int:
    # cur.execute("SELECT COUNT(*) FROM rounds")
    cur.execute("SELECT MAX(id) FROM rounds")
    return cur.fetchone()[0]


def clear_history():
    cur.execute("DELETE FROM rounds")
    cur.execute("DELETE FROM sqlite_sequence WHERE name='rounds'")
    # cur.execute("ALTER TABLE rounds AUTO_INCREMENT = 1")
    conn.commit()
    print("Table cleared.")


def close():
    conn.close()
    print("Database disconnected.")
