import logging
import os
import sqlite3
from typing import Any
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# Configuración de variables de entono
DB_PATH = os.getenv("SQLITE_DB_PATH")
BASE_DIR = Path(__file__).resolve().parent

# Inicialización del MCP Server
mcp = FastMCP("mcp sqlite")

# Configuración de logging para depuración
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler(BASE_DIR / "logs" / "mcp_sqlite.log", encoding="utf-8")],
)

log = logging.getLogger("mcp_sqlite")


# --- Función interna de conexión ---
def sqlite_connection(query: str, params: tuple = (), is_select: bool = False) -> Any:
    if not DB_PATH:
        return "Error: No has configurado la variable SQLITE_DB_PATH en Claude."

    # Verificamos si el archivo realmente existe
    if not os.path.exists(DB_PATH):
        return f"Error: No se encuentra el archivo en {DB_PATH}"

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if is_select:
                return cursor.fetchall()
            conn.commit()
            return "Query executed successfully."
    except sqlite3.IntegrityError as e:
        return f"Error: {str(e)}"
    except (sqlite3.OperationalError, sqlite3.ProgrammingError) as e:
        log.error(f"SQL Error: {str(e)}")
        return f"Error: {str(e)}"
    except Exception as e:
        log.error(f"Unexpected Error: {str(e)} - Query: {query} - Params: {params}")
        return f"Error inesperado: {str(e)}"


# --- HERRAMIENTAS (TOOLS) PARA EL MCP ---


@mcp.tool()
def list_tables() -> list:
    """Lista todos los nombres de las tablas disponibles en la base de datos."""
    query = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"

    return [row[0] for row in sqlite_connection(query, is_select=True)]


@mcp.tool()
def get_table_schema(table_name: str) -> list:
    """Devuelve los nombres de las columnas de una tabla específica."""
    query = f"PRAGMA table_info({table_name})"

    return [row[1] for row in sqlite_connection(query, is_select=True)]


@mcp.tool()
def execute_read_query(query: str, params: tuple = (), limit: int = 20) -> Any:
    """
    Ejecuta consultas de LECTURA (SELECT, WITH/CTE, Joins, etc.).
    Utiliza sentencias preparadas para garantizar la integridad y seguridad.
    Los valores externos deben pasarse exclusivamente mediante marcadores de posición (?)
    en el argumento 'params', evitando la concatenación directa de cadenas.
    """

    _query = query.strip().upper()
    if not (_query.startswith("SELECT") or _query.startswith("WITH")):
        return "Error: Esta función solo admite consultas de lectura."

    safe_query = f"{_query} LIMIT ?"
    safe_params = params + (limit,)

    return sqlite_connection(safe_query, safe_params, is_select=True)


@mcp.tool()
def execute_write_query(query: str, params: tuple = ()) -> str:
    """
    Ejecuta consultas de ESCRITURA (INSERT, UPDATE, DELETE).
    Utiliza sentencias preparadas para garantizar la integridad y seguridad.
    Los valores externos deben pasarse exclusivamente mediante marcadores de posición (?)
    en el argumento 'params', evitando la concatenación directa de cadenas.
    """
    _query = query.strip().upper()
    if _query.startswith("SELECT") or _query.startswith("WITH"):
        return "Error: Usar la función execute_read_query para consultas de lectura."

    sqlite_connection(query, params)
    return "Consulta de escritura ejecutada con éxito."


@mcp.tool()
def create_index(table_name: str, column_name: str) -> str:
    """
    Crea un índice en una columna específica para acelerar las búsquedas.
    Úsalo si las consultas a una tabla grande se vuelven lentas.
    """
    index_name = f"idx_{table_name}_{column_name}"
    query = f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name}({column_name});"

    sqlite_connection(query)

    log.info(f"Índice creado: {index_name} en {table_name}({column_name})")
    return (
        f"Índice {index_name} creado con éxito. Las búsquedas ahora serán más rápidas."
    )


if __name__ == "__main__":
    mcp.run()
    
