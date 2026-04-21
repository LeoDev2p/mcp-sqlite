from pathlib import Path
import os

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Directorio para logs
DIR_LOG = BASE_DIR / "logs"

# Configuración de variables de entono
DB_PATH = os.getenv("SQLITE_DB_PATH")