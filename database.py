from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Dirección de tu base de datos SQLite
# Se creará un archivo llamado "entregas_oscar.db" en tu carpeta principal
SQLALCHEMY_DATABASE_URL = "sqlite:///./entregas_oscar.db"

# 2. El Motor de Conexión
# NOTA: 'check_same_thread': False es una configuración obligatoria y exclusiva 
# para usar SQLite con FastAPI, ya que FastAPI maneja múltiples peticiones a la vez.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. La Sesión
# Esto es lo que usamos en los routers (SessionLocal) para hacer consultas.
# Funciona como una "sala de chat" temporal con la base de datos.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. La Clase Base
# De aquí heredarán todos los modelos (como tu PedidoDB) en el archivo models.py
Base = declarative_base()