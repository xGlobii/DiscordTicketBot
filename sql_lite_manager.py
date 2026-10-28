import sqlite3

class SqLiteManager():
    def __init__(self, db_path: str = "database.sqlite"):
        self.db_path = db_path
        self.initiate_tables()

    def initiate_tables(self) -> None:
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS guild_config (
                guild_id INTEGER PRIMARY KEY,
                support_role_id INTEGER NULL,
                ticket_channel_id INTEGER NULL,
                command_prefix TEXT NOT NULL DEFAULT '!'
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

            cursor.execute(
                """CREATE TABLE IF NOT EXISTS guild_commands(
                guild_id INTEGER,
                command_name TEXT,
                command_type TEXT,
                attributes TEXT NULL,
                required_permission TEXT NULL,
                PRIMARY KEY(guild_id, command_name)
                )
                """
            )

            cursor.execute(
                """CREATE TABLE IF NOT EXISTS guild_counters(
                guild_id INTEGER,
                counter_name TEXT,
                counter_value INTEGER DEFAULT 0,
                PRIMARY KEY(guild_id, counter_name)
                )
                """
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

    def get_tickets(self, user_id: int, offset: int):
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute("""SELECT title, description, created_at, closed_by_id, closed_at FROM tickets WHERE creator_id = ? LIMIT 10 OFFSET ?""", (user_id, offset))
            return cursor.fetchall()

    def save_command(self, guild_id: int, command_name: str, command_type: str, required_permission: str, attributes: str = None):
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute("""INSERT INTO guild_commands (guild_id, command_name, command_type, required_permission, attributes)
            VALUES (?, ? , ?, ?, ?)""", (guild_id, command_name, command_type, required_permission, attributes))

            if (command_type == "counter"):
                cursor.execute("""INSERT INTO guild_counters (guild_id, counter_name) VALUES (?, ?)""", (guild_id, command_name))

    def get_guild_commands(self, guild_id: int):
        with sqlite3.connect(self.db_path) as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute("""SELECT * FROM guild_commands WHERE guild_id = ?""", (guild_id, ))
            return cursor.fetchall()