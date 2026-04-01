# MCP SQLite Server

```
███╗   ███╗ ██████╗██████╗     ███████╗ ██████╗ ██╗     ██╗████████╗███████╗
████╗ ████║██╔════╝██╔══██╗    ██╔════╝██╔═══██╗██║     ██║╚══██╔══╝██╔════╝
██╔████╔██║██║     ██████╔╝    ███████╗██║   ██║██║     ██║   ██║   ███████╗
██║╚██╔╝██║██║     ██╔═══╝     ╚════██║██║   ██║██║     ██║   ██║   ██║════
██║ ╚═╝ ██║╚██████╗██║         ███████║╚██████╔╝███████╗██║   ██║   ███████║
╚═╝     ╚═╝ ╚═════╝╚═╝         ╚══════╝ ╚═════╝ ╚══════╝╚═╝   ╚═╝   ╚══════╝
```


Un servidor **Model Context Protocol (MCP)** profesional para SQLite que permite a modelos de lenguaje consultar, analizar y gestionar bases de datos SQLite de forma segura y eficiente.

## 📋 Descripción

Este MCP proporciona una interfaz segura entre modelos de lenguaje (como Claude) y bases de datos SQLite. Permite:

- **Listar tablas** disponibles en la base de datos
- **Explorar esquemas** de tablas (columnas, tipos de datos)
- **Ejecutar consultas SQL** SELECT robustamente
- **Crear índices** para optimizar rendimiento
- **Logging avanzado** para auditoría y debugging

## 🚀 Requisitos

- **Python 3.12+**
- **[uv](https://docs.astral.sh/uv/)** (gestor de paquetes ultrarrápido)
- SQLite 3.x (incluido por defecto en Python)
- Una base de datos SQLite (.db)

### Instalación de uv

#### Windows

1. Abre **PowerShell** como administrador
2. Ejecuta el instalador:

```powershell
PowerShell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Reinicia tu terminal

**Verifica la instalación en cualquier SO:**

```bash
uv --version
```

## 📦 Instalación del Proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/LeoDev2p/mcp-sqlite.git
cd mcp_sqlite
```

### 2. Instalar dependencias con uv

```bash
uv sync
```

Este comando:
- Crea un entorno virtual (.venv)
- Instala las dependencias del `pyproject.toml`
- Configura FastMCP y MCP automáticamente

### 3. Verificar la instalación

```bash
uv run mcp_sqlite_server.py --help
```

Si todo está correcto, deberías ver la ayuda del servidor MCP.

### 4. Probar el MCP localmente

Para desarrollo y testing, usa `fastmcp dev`:

```bash
fastmcp dev mcp_sqlite_server.py
```

Esto abre un cliente interactivo donde puedes probar las herramientas en tiempo real.

## ⚙️ Configuración en Claude Desktop

1. **Abre o crea** el archivo de configuración:
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS/Linux:** `~/.config/Claude/claude_desktop_config.json`

2. **Añade la siguiente configuración** dentro de la sección `mcpServers`:

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "C:\\Users\\usuario\\.local\\bin\\uv.exe",
      "args": [
        "--directory",
        "/ruta/a/tu/proyecto/mcp_sqlite",
        "run",
        "mcp_sqlite_server.py"
      ],
      "env": {
        "SQLITE_DB_PATH": "/ruta/a/tu/base/datos.db"
      }
    }
  }
}
```

**Nota:** Reemplaza las rutas con las reales de tu sistema. `uv` debe estar en tu PATH después de la instalación.

### Parámetros de configuración

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `command` | Ruta al ejecutable de `uv` | `C:\\Users\\usuario\\.local\\bin\\uv.exe` |
| `args` | Argumentos para ejecutar el servidor | Array con `--directory`, ruta, `run`, `mcp_sqlite_server.py` |
| `SQLITE_DB_PATH` | Ruta completa a la BD (.db) | `C:\\ruta\\a\\tu\\basedatos.db` |

## 🔧 Herramientas disponibles

### 1. `list_tables()`

Lista todos los nombres de las tablas en la base de datos.

**Ejemplo en Claude:**
```
"¿Qué tablas hay disponibles en la base de datos?"
```

**Respuesta esperada:**
```
['movies', 'actors', 'genres', 'ratings']
```

---

### 2. `get_table_schema(table_name: str)`

Devuelve los nombres de las columnas de una tabla específica.

**Parámetros:**
- `table_name` (str): Nombre de la tabla a explorar

**Ejemplo en Claude:**
```
"Dame el esquema de la tabla 'movies'"
```

**Respuesta esperada:**
```
['id', 'title', 'year', 'director', 'rating']
```

---

### 3. `execute_query(sql_query: str)`

Ejecuta una consulta SQL SELECT y devuelve los resultados.

**Parámetros:**
- `sql_query` (str): Consulta SQL válida

**Ejemplo en Claude:**
```
"Ejecuta esta consulta: SELECT title, year FROM movies WHERE year > 2000"
```

**Respuesta esperada:**
```
[('Inception', 2010), ('Interstellar', 2014), ('Oppenheimer', 2023)]
```

**⚠️ Seguridad:**
- Protección contra inyección SQL
- CRUD y consultas avanzadas

---

### 4. `create_index(table_name: str, column_name: str)`

Crea un índice en una columna para acelerar búsquedas en tablas grandes.

**Parámetros:**
- `table_name` (str): Nombre de la tabla
- `column_name` (str): Nombre de la columna

**Ejemplo en Claude:**
```
"Crea un índice en la tabla 'movies' para la columna 'year'"
```

**Respuesta esperada:**
```
"Índice idx_movies_year creado con éxito. Las búsquedas ahora serán más rápidas."
```

---

## ️ Características de Seguridad

### Validación de rutas

```python
if not os.path.exists(DB_PATH):
    return f"Error: No se encuentra el archivo en {DB_PATH}"
```

- Verifica que la base de datos existe
- Evita errores de rutas mal configuradas

### Manejo de errores robusto

```python
try:
    # Ejecución de query
except sqlite3.IntegrityError as e:
    return f"Error: {str(e)}"
except sqlite3.OperationalError as e:
    # Log detallado para debugging
    log.error(f"SQL Error: {str(e)}")
```

### Variables de entorno

La ruta de la BD se configura mediante `SQLITE_DB_PATH` en lugar de estar hardcodeada, mejorando:
- Portabilidad
- Seguridad
- Flexibilidad

## 📊 Sistema de Logging

Los logs se guardan automáticamente en `logs/app.log` para auditoría y debugging.



## 🔄 Actualización

Para actualizar dependencias:

```bash
uv sync --upgrade
```

Para actualizar solo la configuración:

```bash
uv sync
```

## 📝 Desarrollo

### Añadir una nueva herramienta

1. En `mcp_sqlite_server.py`, añade una nueva función con decorador `@mcp.tool()`:

```python
@mcp.tool()
def nueva_herramienta(param: str) -> str:
    """Descripción de qué hace esta herramienta."""
    query = f"SELECT ..."
    return sqlite_connection(query)
```

2. Reinicia Claude Desktop

3. La nueva herramienta estará disponible automáticamente

### Testing local

```bash
uv run mcp_sqlite_server.py
```

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver archivo `LICENSE` para detalles.

## 👤 Autor

Desarrollado para mejorar la integración entre modelos de lenguaje y bases de datos SQLite.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

Si encuentras problemas:

1. Revisa los logs en `logs/app.log`
2. Verifica la configuración en `claude_desktop_config.json`
3. Asegúrate de que la BD existe y es accesible

---

**Versión:** 0.1.0  
**Última actualización:** 2026-03-31
