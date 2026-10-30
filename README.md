# Discord Administration & Support Bot

> **Note:** This project was developed as an academic assignment for university course.

A modular Discord bot written in Python using the `discord.py` library. It provides comprehensive ticket handling, custom commands, and server management tools.

---

## Key features

**Ticket System**
- Persistent UI panels.
- Storing ticket history in a database.
- Log pagination for users using interactive embeds.

**Server Management**
- Fast, command-line management of role access to channels and categories.
- Dynamic channel creators.

**Custom Command System**
- Command management from the database without the need to edit code.
- Support for multiple action types.

**Lightweight Database**
- Uses an optimized `SQLite3` connection.

---

## Technology Stack
- **Language:** Python
- **Library:** `discord.py`
- **Database:** `sqlite3`
- **Environment:** `python-dotenv` for configuration management.

---

## Configuration and Setup

1. Clone the repository to your server.
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file and set the environment variables:
   ```env
   DISCORD_TOKEN=your_bot_token_here
   TICKETS_PER_PAGE=5
   ```
4. Run the bot:
   ```bash
   python main.py
   ```

---

### User Guide
The bot operates using native slash commands and interactive UI components, which means users don’t need to learn any complicated syntax.

- **`/prepare`** – Generates a panel on the selected channel that allows users to open new tickets.
- **`/add_access` and `/remove_access`** – Commands that allow you to instantly grant or revoke access to a selected text channel, voice channel, or an entire category for a specific server role.
- **Ticket Management** – When a ticket is opened, the bot creates a private communication channel. Tickets are closed using a button in the bot’s interface.
- **Log Viewing** – The bot generates formatted summaries of closed and active tickets in the form of paginated embeds with navigation buttons.

### API & Application Architecture
The project actively uses Discord’s public APIs via the asynchronous `discord.py` library.
- **Communication:** The bot listens for events and user interactions (commands, button clicks, selections from dropdown lists) via a stable WebSocket connection.
- **Component-Based UI:** Navigation logic (e.g., `PaginationView`) does not rely on deleting and sending new messages, but rather on immediate `edit_message` requests to the Discord API, updating only the view (`embed` and the state of `discord.ui.View`). Components are proactively deactivated once page index limits are reached.

### Database Schema
The application is based on a local, optimized **SQLite3** relational database. Key data, such as ticket history, is stored in a structured format, which enables analytics and pagination.
Example outline of the log structure:
- `guild_id` (INT) / `user_id` (INT) – Unique identifiers for servers and users.
- `title` (TEXT) / `description` (TEXT) – Ticket content and subject.
- `created_at` (TIMESTAMP) / `closed_at` (TIMESTAMP) / `closed_by_id` (INT) – Timestamps and the ID of the person who closed the ticket.
By using queries with the `LIMIT` and `OFFSET` clauses, the application retrieves from the database only those records that are currently being displayed to the user.

## Architecture

The bot uses a modular structure, which allows for the logical separation of functions. User interfaces are implemented using an object-oriented approach with `discord.ui.View`, ensuring full interactivity without cluttering the bot’s main thread.