import sqlite3

from constants import RoundResult
from record import RoundRecord


def serialize_round_result(result: RoundResult, won_on_time: bool) -> int:
    return int(result) + (16 if won_on_time else 0)


def deserialize_round_result(result) -> (int, bool):
    won_on_time = result >= 16
    return result % 16, won_on_time


# Creates a new database file if it doesn’t exist.
conn: sqlite3.Connection = sqlite3.connect("rounds.sqlite")
cur: sqlite3.Cursor = conn.cursor()


def start():
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


def get_round_count() -> int:
    cur.execute("SELECT COUNT(*) FROM rounds")
    return cur.fetchone()[0]


def clear_history():
    cur.execute("DELETE FROM rounds")
    conn.commit()
    print("Table cleared.")


def close():
    conn.close()
    print("Database disconnected.")
