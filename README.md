# Discord Administration & Support Ecosystem

> **Note:** This project was developed as an academic assignment for a university course.

A comprehensive, full-stack ecosystem for Discord server management. It consists of a modular Discord bot written in Python and a Web Dashboard powered by a React Single Page Application (SPA) and an ASP.NET Core Web API. 

The project provides comprehensive ticket handling, dynamic custom command management, server management tools, and an interactive web interface for server administrators.

---

## Key Features

**Web Dashboard & API**
- **Secure Authentication:** Integrated Discord OAuth2 flow utilizing highly secure, HTTP-only cookies.
- **Performance Optimized:** Employs `IMemoryCache` (5-minute expiration) to minimize Discord API rate limits and speed up dashboard load times.
- **Server Analytics:** Quick overview of active/resolved tickets and custom command statistics via the dashboard.
- **Custom Command Management:** Add and configure new bot commands directly from the web interface.

**Discord Bot**
- **Ticket System:** Persistent UI panels, interactive embeds, database history, and log pagination.
- **Server Management:** Fast, command-line management of role access to channels and categories, and dynamic channel creators.
- **Custom Command System:** Reads dynamically created commands from the database and supports multiple action types.

---

## Technology Stack

**Frontend (Web Dashboard)**
- **Framework:** React with TypeScript
- **State Management:** React Context API (`AuthProvider`) for global authentication state.
- **Routing:** React Router with protected routes for unauthenticated users.

**Backend (REST API)**
- **Framework:** C# / ASP.NET Core
- **Architecture:** Clean Architecture / business logic separated into Services.
- **ORM:** Entity Framework Core.

**Discord Bot**
- **Language:** Python
- **Library:** `discord.py`
- **Database:** `SQLite3` integrated with both Bot and Web API.
- **Environment:** `python-dotenv`.

---

## Configuration and Setup
> **Note:** To make sure everything works properly, run the bot first so that it generates the database file.
### 1. Bot Setup
1. Clone the repository.
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the bot directory:
   ```env
   DISCORD_TOKEN=your_bot_token_here
   TICKETS_PER_PAGE=5
   ```
4. Run the bot:
   ```bash
   python main.py
   ```

### 2. Backend (ASP.NET Core API) Setup
1. Navigate to the API project directory.
2. Update the `appsettings.json` with your Discord Client ID, Client Secret.
> **Note:** The database connection string is hardcoded in the application configuration to point to the shared SQLite file (../../shared/database.sqlite).
3. Run the API:
   ```bash
   dotnet run
   ```

### 3. Frontend (React) Setup
1. Navigate to the frontend directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```

---

## User Guide

### Bot Interactions
The bot operates using native slash commands and interactive UI components, meaning users don’t need to learn complicated syntax.
- **`/prepare`** – Generates a panel on the selected channel that allows users to open new tickets.
- **`/add_access` & `/remove_access`** – Instantly grant or revoke access to a selected text/voice channel or an entire category for a specific server role.
- **Ticket Management** – Creates private communication channels for tickets, closed via a button in the bot’s interface.
- **Log Viewing** – Generates formatted summaries of closed and active tickets as paginated embeds with navigation buttons.

### Web Dashboard
- Navigate to the frontend URL.
- Click **Login via Discord** to authenticate securely.
- Access the **Dashboard** to view server statistics.
- Use the **Commands** panel to dynamically add new commands to the bot.

---

## Architecture & Design Patterns

### API & Application Architecture
- **Clean Architecture & DRY:** Business logic, caching, and data fetching are encapsulated within injected Services (e.g., `AuthService`).
- **OAuth2 Flow:** The backend handles code exchange with Discord, sets secure HTTP-only cookies (`access_token`, `refresh_token`), and redirects the user. The React frontend relies on these cookies to fetch cached session data via the `/me` endpoint.
- **CI/CD Pipeline:** The project utilizes GitHub Actions for Continuous Integration. Pushing code or publishing a release triggers automated builds and creates tracking issues automatically.

### Bot Architecture (Python)
- **Component-Based UI:** Navigation logic (e.g., `PaginationView`) does not rely on deleting and sending new messages. It uses immediate `edit_message` requests to update the view, keeping the Discord API usage low.
- **Asynchronous Processing:** Built entirely on asynchronous methods (`async`/`await`) ensuring the main bot thread is never blocked.

### Database Schema
The application uses a relational database (SQLite). Key data is stored in a structured format allowing seamless communication between the Python Bot and the C# API.
Example structures:
- `Guilds` / `Users` – Unique identifiers for servers and users.
- `Tickets` – Contains `title`, `description`, `created_at`, `closed_at`, and `status`.
- `Commands` – Stores dynamically created commands (`CommandName`, `Description`, `RequiredPermission`) that the API inserts and the Bot reads.
