import sqlite3
import os

class SqLiteManager():
    def __init__(self, db_path: str = "../shared/database.sqlite"):
        self.db_path = db_path
        self.initiate_tables()

    def initiate_tables(self) -> None:
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS guild_config (
                guild_id BIGINT PRIMARY KEY,
                support_role_id BIGINT NULL,
                ticket_channel_id BIGINT NULL,
                command_prefix TEXT NOT NULL DEFAULT '!'
                )"""
            )

            cursor.execute(
                """CREATE TABLE IF NOT EXISTS tickets(
                ticket_id BIGINT PRIMARY KEY,
                guild_id BIGINT,
                creator_id BIGINT,
                title TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                closed_by_id BIGINT NULL,
                closed_at TIMESTAMP NULL,
                status TEXT,
                is_claimed INTEGER DEFAULT 0
                )
                """
            )

            cursor.execute(
                """CREATE TABLE IF NOT EXISTS guild_commands(
                guild_id BIGINT,
                command_name TEXT,
                command_type TEXT,
                attributes TEXT NULL,
                required_permission TEXT NULL,
                description TEXT NULL,
                PRIMARY KEY(guild_id, command_name)
                )
                """
            )

            cursor.execute(
                """CREATE TABLE IF NOT EXISTS guild_counters(
                guild_id BIGINT,
                counter_name TEXT,
                counter_value INTEGER DEFAULT 0,
                PRIMARY KEY(guild_id, counter_name)
                )
                """
            )

            cursor.execute(
                """CREATE TABLE IF NOT EXISTS heartbeat(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )"""
            )

    def make_heartbeat(self):
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute(
                """INSERT INTO heartbeat DEFAULT VALUES"""
            )

    def save_config(self, guild_id: int, support_role_id: int, ticket_channel_id: int) -> None:
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute(
                """INSERT INTO guild_config (guild_id, support_role_id, ticket_channel_id) VALUES (?, ?, ?) ON CONFLICT(guild_id)
                DO UPDATE SET
                support_role_id = excluded.support_role_id,
                ticket_channel_id = excluded.ticket_channel_id
                """
                , (guild_id, support_role_id, ticket_channel_id)
            )

    def update_command_prefix(self, guild_id: int, command_prefix: str) -> None:
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute(
                """INSERT OR REPLACE INTO guild_config (guild_id, command_prefix) VALUES (?, ?) ON CONFLICT(guild_id)
                DO UPDATE SET
                command_prefix = excluded.command_prefix
                """, (guild_id, command_prefix)
            )

    def save_ticket(self, ticket_id: int, guild_id: int, creator_id: int, title: str, description: str, status: str = "open"):
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute(
                """ INSERT INTO tickets (ticket_id, guild_id, creator_id, title, description, status) VALUES (?, ?, ?, ?, ?, ?)""",
                (ticket_id, guild_id, creator_id, title, description, status)
            )

    def get_ticket(self, ticket_id: int, guild_id: int):
        with sqlite3.connect(self.db_path) as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(
                """SELECT is_claimed, creator_id FROM tickets WHERE ticket_id = ? AND guild_id = ?""", (ticket_id, guild_id)
            )
            return cursor.fetchone()

    def close_ticket(self, ticket_id: int, closed_by_id: int, status: str):
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute("""UPDATE tickets SET closed_by_id = ?, closed_at = CURRENT_TIMESTAMP, status = ? WHERE ticket_id = ?""", (closed_by_id, status, ticket_id))

    def claim_ticket(self, ticket_id: int, guild_id: int):
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute(
                """UPDATE tickets SET is_claimed = 1 WHERE ticket_id = ? AND guild_id = ?""", (ticket_id, guild_id)
            )

    def get_config(self, guild_id: int):
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute("""SELECT support_role_id, ticket_channel_id FROM guild_config WHERE guild_id = ?""", (guild_id,))
            return cursor.fetchone()

    def get_guild_prefix(self, guild_id: int):
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute("""SELECT command_prefix FROM guild_config WHERE guild_id = ?""", (guild_id, ))
            result = cursor.fetchone()
            return result[0] if result else '!'

    def get_prefixes(self):
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute("""SELECT guild_id, command_prefix FROM guild_config""")
            return dict(cursor.fetchall())

    def get_tickets(self, guild_id: int, user_id: int, offset: int):
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute("""SELECT title, description, created_at, closed_by_id, closed_at FROM tickets WHERE creator_id = ? AND guild_id = ? LIMIT ? OFFSET ?""", (user_id, guild_id, int(os.getenv('RECORDS_PER_PAGE', '5')), offset))
            return cursor.fetchall()

    def save_command(self, guild_id: int, command_name: str, command_type: str, required_permission: str, attributes: str = None, description: str = None):
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute("""INSERT INTO guild_commands (guild_id, command_name, command_type, required_permission, attributes, description)
            VALUES (?, ? , ?, ?, ?, ?)""", (guild_id, command_name, command_type, required_permission, attributes, description))

            if (command_type == "counter"):
                cursor.execute("""INSERT INTO guild_counters (guild_id, counter_name) VALUES (?, ?)""", (guild_id, command_name))

    def get_guild_commands(self, guild_id: int):
        with sqlite3.connect(self.db_path) as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute("""SELECT * FROM guild_commands WHERE guild_id = ?""", (guild_id, ))
            return cursor.fetchall()

    def get_custom_command(self, guild_id: int, command_name: str):
        with sqlite3.connect(self.db_path) as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute("""SELECT * FROM guild_commands WHERE guild_id = ? AND command_name = ?""", (guild_id, command_name))
            return cursor.fetchone()
    def get_and_increment_counter(self, guild_id: int, counter_name: str):
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute("""UPDATE guild_counters SET counter_value = counter_value + 1 WHERE guild_id = ? AND counter_name = ?
            RETURNING counter_value""", (guild_id, counter_name))
            return cursor.fetchone()[0]

    def get_all_user_tickets(self, guild_id: int, user_id: int):
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute("""SELECT COUNT(ticket_id) FROM tickets WHERE guild_id = ? AND creator_id = ?""", (guild_id, user_id))
            return cursor.fetchone()[0]