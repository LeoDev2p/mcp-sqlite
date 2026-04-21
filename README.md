# MCP SQLite Server

```
███╗   ███╗ ██████╗██████╗     ███████╗ ██████╗ ██╗     ██╗████████╗███████╗
████╗ ████║██╔════╝██╔══██╗    ██╔════╝██╔═══██╗██║     ██║╚══██╔══╝██╔════╝
██╔████╔██║██║     ██████╔╝    ███████╗██║   ██║██║     ██║   ██║   ███████╗
██║╚██╔╝██║██║     ██╔═══╝     ╚════██║██║   ██║██║     ██║   ██║   ██║════
██║ ╚═╝ ██║╚██████╗██║         ███████║╚██████╔╝███████╗██║   ██║   ███████║
╚═╝     ╚═╝ ╚═════╝╚═╝         ╚══════╝ ╚═════╝ ╚══════╝╚═╝   ╚═╝   ╚══════╝
                                V 0.2.0
```

A professional **Model Context Protocol (MCP)** server for SQLite with **full async support** that enables language models to query, analyze, and manage SQLite databases safely and efficiently.

## Overview

This MCP provides a secure, fully asynchronous interface between language models (such as Claude) and SQLite databases. It enables:

- **List tables** available in the database
- **Explore schemas** of tables (columns, data types)
- **Execute SQL queries** robustly with prepared statements
- **Create indexes** to optimize performance
- **Advanced async logging** with log rotation and disk management

## Requirements

- **Python 3.12+**
- **[uv](https://docs.astral.sh/uv/)** (ultrafast package manager)
- SQLite 3.x (included by default in Python)
- A SQLite database (.db)

### Installing uv

#### Windows

1. Open **PowerShell** as administrator
2. Run the installer:

```powershell
PowerShell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Restart your terminal

**Verify installation on any OS:**

```bash
uv --version
```

## Project Installation

### 1. Clone the repository

```bash
git clone https://github.com/LeoDev2p/mcp-sqlite.git
cd mcp_sqlite
```

### 2. Install dependencies with uv

```bash
uv sync
```

This command:
- Creates a virtual environment (.venv)
- Installs dependencies from `pyproject.toml`
- Automatically configures FastMCP and MCP

### 3. Verify the installation

```bash
uv run server.py --help
```

If everything is correct, you should see the MCP server help.

### 4. Test the MCP locally

For development and testing, use `fastmcp dev`:

```bash
fastmcp dev server.py
```

This opens an interactive client where you can test the tools in real time.

## Architecture Overview

### Async-First Design

The server is built entirely with **async/await** patterns for optimal performance:

- **Asynchronous Connection Pool**: Uses `aiosqlite` for non-blocking database access
- **Concurrent Tool Execution**: Multiple queries can be processed simultaneously without blocking
- **Resource Management**: Automatic connection cleanup with context managers (`async with`)
- **Thread-Safe Operations**: Built-in support for concurrent requests from language models

### Database Connection Flow

```
FastMCP Server (async)
    ↓
    async sqlite_connection() function
    ↓
    aiosqlite.connect() (non-blocking)
    ↓
    SQL Execution (prepared statements)
    ↓
    Response (cached or streamed)
```

## � Tools Reference

All tools are **fully asynchronous** and use prepared statements for security:

### 1. `list_tables()`

Lists all table names in the database.

**Type:** Async Read  
**Example in Claude:**
```
"What tables are available in the database?"
```

**Expected response:**
```
['movies', 'actors', 'genres', 'ratings']
```

---

### 2. `get_table_schema(table_name: str)`

Returns the column names and types of a specific table.

**Parameters:**
- `table_name` (str): Name of the table to explore

**Type:** Async Read  
**Example in Claude:**
```
"Show me the schema of the 'movies' table"
```

**Expected response:**
```
['id', 'title', 'year', 'director', 'rating']
```

---

### 3. `execute_read_query(query: str, params: tuple = (), limit: int = 20)`

Executes READ queries (SELECT, WITH/CTE, JOINS, etc.) safely with prepared statements.

**Parameters:**
- `query` (str): Valid SQL SELECT or WITH query
- `params` (tuple): Values for placeholders to prevent SQL injection (default: empty)
- `limit` (int): Maximum rows to return (default: 20)

**Type:** Async Read  
**Security Features:**
- Prepared statements prevent SQL injection
- Automatic LIMIT protection prevents data overload
- Only supports SELECT and WITH queries
- Validates query structure before execution

**Example in Claude:**
```
"Execute this query: SELECT title, year FROM movies WHERE year > ?"
With params: (2000,)
```

**Expected response:**
```
[('Inception', 2010), ('Interstellar', 2014), ('Oppenheimer', 2023)]
```

---

### 4. `execute_write_query(query: str, params: tuple = ())`

Executes WRITE queries (INSERT, UPDATE, DELETE) safely with prepared statements.

**Parameters:**
- `query` (str): Valid SQL INSERT, UPDATE, or DELETE query
- `params` (tuple): Values for placeholders to prevent SQL injection (default: empty)

**Type:** Async Write  
**Security Features:**
- Prepared statements prevent SQL injection
- Blocks accidental SELECT queries from being executed here
- Auto-commits transactions
- Comprehensive error handling

**Example in Claude:**
```
"Insert a new movie with title 'Avatar' and year 2022"
Query: INSERT INTO movies (title, year) VALUES (?, ?)
With params: ('Avatar', 2022)
```

**Expected response:**
```
"Write query executed successfully."
```

---

### 5. `create_index(table_name: str, column_name: str)`

Creates an index on a column to speed up searches on large tables.

**Parameters:**
- `table_name` (str): Name of the table
- `column_name` (str): Name of the column to index

**Type:** Async Write  
**Performance Impact:** Significantly speeds up WHERE clause filtering on indexed columns

**Example in Claude:**
```
"Create an index on the 'movies' table for the 'year' column"
```

**Expected response:**
```
"Index idx_movies_year created successfully. Searches will now be faster."
```

---

## Security Features

### Path Validation

```python
if not os.path.exists(DB_PATH):
    return f"Error: File not found at {DB_PATH}"
```

- Verifies that the database file exists
- Prevents misconfiguration errors

### Robust Error Handling

```python
try:
    # Query execution
except sqlite3.IntegrityError as e:
    return f"Error: {str(e)}"
except sqlite3.OperationalError as e:
    # Detailed logging for debugging
    log.error(f"SQL Error: {str(e)}")
```

### Environment Variables

The database path is configured via `SQLITE_DB_PATH` instead of being hardcoded, improving:
- Portability
- Security
- Flexibility

## Logging System

Logs are automatically saved to `logs/server.log` for auditing and debugging.

## Updating

To update dependencies:

```bash
uv sync --upgrade
```

To update only the configuration:

```bash
uv sync
```

## Development

### Adding a New Tool

1. In `server.py`, add a new function with the `@mcp.tool()` decorator:

```python
@mcp.tool()
async def new_tool(param: str) -> str:
    """Description of what this tool does."""
    query = f"SELECT ..."
    return await sqlite_connection(query)
```

---

## Configuration for Claude Desktop & Antigravity

The MCP server configuration is **identical for all three platforms** — only the configuration file location changes.

### Configuration File Locations

| Platform | File Location |
|----------|---------------|
| **Claude Desktop** | `%APPDATA%\Claude\claude_desktop_config.json` (Windows) or `~/.config/Claude/claude_desktop_config.json` (macOS/Linux) |
| **Antigravity** | `%APPDATA%\Antigravity\mcp_config.json` (Windows) or `~/.config/Antigravity/mcp_config.json` (macOS/Linux) |

### Setup Instructions

1. **Open or create** the appropriate configuration file for your platform (see table above)

2. **Add the following JSON configuration** within the `mcpServers` section:

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\path\\to\\mcp_sqlite",
        "run",
        "server.py"
      ],
      "env": {
        "SQLITE_DB_PATH": "C:\\path\\to\\your\\database.db"
      }
    }
  }
}
```

**Configuration Parameters:**

| Parameter | Description | Example |
|-----------|-------------|---------|
| `command` | The command to run (uv package manager) | `uv` |
| `--directory` | Path to the mcp_sqlite project directory | `C:\\Users\\user\\mcp_sqlite` or `/home/user/mcp_sqlite` |
| `SQLITE_DB_PATH` | Full absolute path to the SQLite database file | `C:\\Users\\user\\databases\\app.db` |

**Platform-Specific Path Examples:**

- **Windows**: `C:\\Users\\YourName\\path\\to\\database.db`
- **macOS/Linux**: `/home/username/path/to/database.db`

3. **Restart the application** (Claude Desktop or Antigravity) for changes to take effect
4. The SQLite tools will be available in the tool menu immediately

## Local Testing & Development

### Test with FastMCP Dev Mode

For interactive testing during development:

```bash
fastmcp dev server.py
```

This opens an interactive client where you can:
- Test async tools in real-time
- See detailed execution logs
- Debug parameters and responses

### Example Test Session

```bash
$ fastmcp dev server.py

# In the interactive shell:
>>> await list_tables()
['users', 'posts', 'comments']

>>> await get_table_schema('users')
['id', 'name', 'email', 'created_at']

>>> await execute_read_query('SELECT * FROM users LIMIT 5')
[...]
```

## 🔧 Advanced: Extending the Server

To add new async tools:

1. Open `src/sqlite_mcp/server.py`
2. Add a new `@mcp.tool()` decorated async function:

```python
@mcp.tool()
async def my_new_tool(param: str) -> str:
    """Description of what this tool does."""
    query = "SELECT ..."
    result = await sqlite_connection(query, is_select=True)
    return result
```

3. Restart Claude Desktop
4. The new tool will be available automatically

### Logging in Custom Tools

Use the logger to track tool execution:

```python
log.info(f"Processing query: {query}")
try:
    result = await sqlite_connection(query)
except Exception as e:
    log.error(f"Tool error: {str(e)}")
    raise
```

## Contributions

Contributions are welcome. Please:

1. Fork the repository
2. Create a branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Support & Troubleshooting

### Check Logs

All activity is logged to `logs/server.log`:

```bash
# View recent logs
tail -f logs/server.log

# On Windows PowerShell
Get-Content logs/server.log -Tail 20 -Wait
```

### Common Issues

**Issue:** `SQLITE_DB_PATH not found`  
**Solution:** Verify the path is correct and the database file exists

**Issue:** Slow queries  
**Solution:** Use `create_index()` on frequently searched columns

**Issue:** "Connection refused"  
**Solution:** Ensure Claude Desktop is restarted after config changes

---

**Version:** 0.2.0  
**Last updated:** 2026-04-21
