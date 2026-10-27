import sqlite3

class SqLiteManager():
    def __init__(self, db_path: str = "database.sqlite"):
        self.db_path = db_path
        self.initiate_tables()

    def save_config(self, guild_id: int, support_role_id: int, ticket_channel_id: int) -> None:
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute(
                """INSERT OR REPLACE INTO config (guild_id, support_role_id, ticket_channel_id) VALUES (?, ?, ?)"""
                , (guild_id, support_role_id, ticket_channel_id)
            )

    def save_ticket(self, ticket_id: int, guild_id: int, creator_id: int, title: str, description: str):
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute(
                """ INSERT INTO tickets (ticket_id, guild_id, creator_id, title, description) VALUES (?, ?, ?, ?, ?)""",
                (ticket_id, guild_id, creator_id, title, description)
            )

    def close_ticket(self, ticket_id: int, closed_by_id: int):
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute("""UPDATE tickets SET closed_by_id = ?, closed_at = CURRENT_TIMESTAMP WHERE ticket_id = ?""", (closed_by_id, ticket_id))

    def initiate_tables(self) -> None:
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS config (
                guild_id INTEGER PRIMARY KEY,
                support_role_id INTEGER,
                ticket_channel_id INTEGER
                )"""
            )

            cursor.execute(
                """CREATE TABLE IF NOT EXISTS tickets(
                ticket_id INTEGER PRIMARY KEY,
                guild_id INTEGER,
                creator_id INTEGER,
                title TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                closed_by_id INTEGER NULL,
                closed_at TIMESTAMP NULL
                )
                """
            )

    def get_config(self, guild_id: int):
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute("""SELECT support_role_id, ticket_channel_id FROM config WHERE guild_id = ?""", (guild_id,))
            return cursor.fetchone()

    def get_tickets(self, user_id: int, offset: int):
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute("""SELECT title, description, created_at, closed_by_id, closed_at FROM tickets WHERE creator_id = ? LIMIT 10 OFFSET ?""", (user_id, offset))
            return cursor.fetchall()