import logging
import os
import sqlite3

from mcp.server.fastmcp import FastMCP

# Configuración de variables de entono
DB_PATH = os.getenv("SQLITE_DB_PATH")

# Inicialización del MCP Server
mcp = FastMCP("mcp sqlite")

# Configuración de logging para depuración
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("logs/mcp_sqlite.log", encoding="utf-8")
    ]

)

log = logging.getLogger("mcp_sqlite")

# --- Función interna de conexión ---
def sqlite_connection(query: str, params: tuple = (), is_select: bool = True):
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
        log.error(f"SQL Error: {str(e)} - Query: {query} - Params: {params}")
        return f"Error: {str(e)}"
    except Exception as e:
        log.error(f"Unexpected Error: {str(e)} - Query: {query} - Params: {params}")
        return f"Error inesperado: {str(e)}"


# --- HERRAMIENTAS (TOOLS) PARA EL MCP ---

@mcp.tool()
def list_tables() -> list:
    """Lista todos los nombres de las tablas disponibles en la base de datos."""
    query = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"

    return [row[0] for row in sqlite_connection(query)]


@mcp.tool()
def get_table_schema(table_name: str) -> list:
    """Devuelve los nombres de las columnas de una tabla específica."""
    query = f"PRAGMA table_info({table_name})"
    
    return [row[1] for row in sqlite_connection(query)]


@mcp.tool()
def execute_sql(sql_query: str, limit: int = 50) -> str | list:
    """
    Ejecuta cualquier comando SQL (SELECT, INSERT, UPDATE, DELETE).
    Si es un SELECT, aplica un límite automático de resultados.
    """
    query_upper = sql_query.strip().upper()
    
    if query_upper.startswith("SELECT"):
        clean_query = sql_query.strip().rstrip(";")
        final_query = f"{clean_query} LIMIT {limit}"
        return sqlite_connection(final_query, is_select=True)
    
    else:
        return sqlite_connection(sql_query, is_select=False)

@mcp.tool()
def create_index(table_name: str, column_name: str) -> str:
    """
    Crea un índice en una columna específica para acelerar las búsquedas.
    Úsalo si las consultas a una tabla grande se vuelven lentas.
    """
    index_name = f"idx_{table_name}_{column_name}"
    query = f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name}({column_name});"
    
    result = sqlite_connection(query, is_select=False)
    
    log.info(f"Índice creado: {index_name} en {table_name}({column_name})")
    return f"Índice {index_name} creado con éxito. Las búsquedas ahora serán más rápidas."



if __name__ == "__main__":
    mcp.run()
