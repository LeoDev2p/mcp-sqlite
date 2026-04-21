import os
import aiosqlite
from typing import Any

from mcp.server.fastmcp import FastMCP
from src.setting.config import DB_PATH
from src.setting.logger import get_logger


# Inicialización del MCP Server
mcp = FastMCP("mcp sqlite")

log = get_logger("mcp_sqlite")


# --- Función asincrona de conexión ---
async def sqlite_connection(query: str, params: tuple = (), is_select: bool = False) -> Any:
    if not DB_PATH:
        return "Error: You have not configured the SQLITE_DB_PATH variable in Claude."
    # Verificamos si el archivo realmente existe
    if not os.path.exists(DB_PATH):
        return f"Error: File not found in {DB_PATH}"

    try:
        async with aiosqlite.connect(DB_PATH) as conn:
            async with conn.execute(query, params) as cursor:
                if is_select:
                    return await cursor.fetchall()
                
                await conn.commit()

                return "Query executed successfully."
    except aiosqlite.IntegrityError as e:
        return f"Error: {str(e)}"
    except (aiosqlite.OperationalError, aiosqlite.ProgrammingError) as e:
        log.error(f"SQL Error: {str(e)}")
        return f"Error: {str(e)}"
    except Exception as e:
        log.error(f"Unexpected Error: {str(e)} - Query: {query} - Params: {params}")
        return f"Unexpected error: {str(e)}"


# --- HERRAMIENTAS (TOOLS) PARA EL MCP ---


@mcp.tool()
async def list_tables() -> list:
    """Returns a list of all table names available in the database."""
    query = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"

    return [row[0] for row in await sqlite_connection(query, is_select=True)]


@mcp.tool()
async def get_table_schema(table_name: str) -> list:
    """Returns the names of the columns of a specific table."""
    query = f"PRAGMA table_info({table_name})"

    return [row[1] for row in await sqlite_connection(query, is_select=True)]


@mcp.tool()
async def execute_read_query(query: str, params: tuple = (), limit: int = 20) -> Any:
    """
    Executes READ queries (SELECT, WITH/CTE, JOINS, etc.).
    Uses prepared statements to ensure data integrity and security.
    External values must be passed exclusively using placeholders (?) in the 'params' argument, avoiding direct string concatenation.
    """

    _query = query.strip().upper()
    if not (_query.startswith("SELECT") or _query.startswith("WITH")):
        return "Error: This function only supports read queries."

    safe_query = f"{_query} LIMIT ?"
    safe_params = params + (limit,)

    return await sqlite_connection(safe_query, safe_params, is_select=True)


@mcp.tool()
async def execute_write_query(query: str, params: tuple = ()) -> str:
    """
    Executes WRITE queries (INSERT, UPDATE, DELETE).
    Uses prepared statements to ensure data integrity and security.
    External values must be passed exclusively using placeholders (?) in the 'params' argument, preventing direct string concatenation.
    """
    _query = query.strip().upper()
    if _query.startswith("SELECT") or _query.startswith("WITH"):
        return "Error: Using the execute_read_query function for read queries."

    await sqlite_connection(query, params)
    return "Write query executed successfully."


@mcp.tool()
async def create_index(table_name: str, column_name: str) -> str:
    """
    Create an index on a specific column to speed up searches.
    Use this if queries to a large table become slow.
    """
    index_name = f"idx_{table_name}_{column_name}"
    query = f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name}({column_name});"

    await sqlite_connection(query)

    log.info(f"Index created: {index_name} in {table_name}({column_name})")
    return f"Index {index_name} created successfully. Searches will now be faster."


if __name__ == "__main__":
    mcp.run()
