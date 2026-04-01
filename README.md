# MCP SQLite Server

```
███╗   ███╗ ██████╗██████╗     ███████╗ ██████╗ ██╗     ██╗████████╗███████╗
████╗ ████║██╔════╝██╔══██╗    ██╔════╝██╔═══██╗██║     ██║╚══██╔══╝██╔════╝
██╔████╔██║██║     ██████╔╝    ███████╗██║   ██║██║     ██║   ██║   ███████╗
██║╚██╔╝██║██║     ██╔═══╝     ╚════██║██║   ██║██║     ██║   ██║   ██║════
██║ ╚═╝ ██║╚██████╗██║         ███████║╚██████╔╝███████╗██║   ██║   ███████║
╚═╝     ╚═╝ ╚═════╝╚═╝         ╚══════╝ ╚═════╝ ╚══════╝╚═╝   ╚═╝   ╚══════╝
```

A professional **Model Context Protocol (MCP)** server for SQLite that enables language models to query, analyze, and manage SQLite databases safely and efficiently.

## 📋 Overview

This MCP provides a secure interface between language models (such as Claude) and SQLite databases. It enables:

- **List tables** available in the database
- **Explore schemas** of tables (columns, data types)
- **Execute SQL queries** robustly
- **Create indexes** to optimize performance
- **Advanced logging** for auditing and debugging

## 🚀 Requirements

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

## 📦 Project Installation

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
uv run mcp_sqlite_server.py --help
```

If everything is correct, you should see the MCP server help.

### 4. Test the MCP locally

For development and testing, use `fastmcp dev`:

```bash
fastmcp dev mcp_sqlite_server.py
```

This opens an interactive client where you can test the tools in real time.

## ⚙️ Claude Desktop Configuration

1. **Open or create** the configuration file:
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS/Linux:** `~/.config/Claude/claude_desktop_config.json`

2. **Add the following configuration** within the `mcpServers` section:

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "C:\\Users\\usuario\\.local\\bin\\uv.exe",
      "args": [
        "--directory",
        "/path/to/your/mcp_sqlite",
        "run",
        "mcp_sqlite_server.py"
      ],
      "env": {
        "SQLITE_DB_PATH": "/path/to/your/database.db"
      }
    }
  }
}
```

**Note:** Replace the paths with the actual paths on your system. `uv` must be in your PATH after installation.

### Configuration Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `command` | Path to the `uv` executable | `C:\\Users\\usuario\\.local\\bin\\uv.exe` |
| `args` | Arguments to run the server | Array with `--directory`, path, `run`, `mcp_sqlite_server.py` |
| `SQLITE_DB_PATH` | Full path to the DB file (.db) | `C:\\path\\to\\your\\database.db` |

## 🔧 Available Tools

### 1. `list_tables()`

Lists all table names in the database.

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

Returns the column names of a specific table.

**Parameters:**
- `table_name` (str): Name of the table to explore

**Example in Claude:**
```
"Show me the schema of the 'movies' table"
```

**Expected response:**
```
['id', 'title', 'year', 'director', 'rating']
```

---

### 3. `execute_query(sql_query: str)`

Executes a SQL query and returns the results.

**Parameters:**
- `sql_query` (str): Valid SQL query

**Example in Claude:**
```
"Execute this query: SELECT title, year FROM movies WHERE year > 2000"
```

**Expected response:**
```
[('Inception', 2010), ('Interstellar', 2014), ('Oppenheimer', 2023)]
```

**⚠️ Security:**
- Protection against SQL injection
- CRUD and advanced queries supported

---

### 4. `create_index(table_name: str, column_name: str)`

Creates an index on a column to speed up searches on large tables.

**Parameters:**
- `table_name` (str): Name of the table
- `column_name` (str): Name of the column

**Example in Claude:**
```
"Create an index on the 'movies' table for the 'year' column"
```

**Expected response:**
```
"Index idx_movies_year successfully created. Searches will now be faster."
```

---

## 🔐 Security Features

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

## 📊 Logging System

Logs are automatically saved to `logs/app.log` for auditing and debugging.

## 🔄 Updating

To update dependencies:

```bash
uv sync --upgrade
```

To update only the configuration:

```bash
uv sync
```

## 📝 Development

### Adding a New Tool

1. In `mcp_sqlite_server.py`, add a new function with the `@mcp.tool()` decorator:

```python
@mcp.tool()
def new_tool(param: str) -> str:
    """Description of what this tool does."""
    query = f"SELECT ..."
    return sqlite_connection(query)
```

2. Restart Claude Desktop

3. The new tool will be available automatically

### Local Testing

```bash
uv run mcp_sqlite_server.py
```

## 📄 License

This project is under the MIT license. See the `LICENSE` file for details.

## 👤 Author

Developed to improve the integration between language models and SQLite databases.

## 🤝 Contributions

Contributions are welcome. Please:

1. Fork the repository
2. Create a branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

If you encounter issues:

1. Check the logs in `logs/app.log`
2. Verify the configuration in `claude_desktop_config.json`
3. Make sure the database exists and is accessible

---

**Version:** 0.1.0  
**Last updated:** 2026-03-31
