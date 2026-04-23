from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Importamos los modelos y la base de datos desde la carpeta principal
import models
from database import SessionLocal

# 1. Creamos el "Departamento" del Administrador
# Nota: El prefijo "/admin" y los tags los pondremos en el main.py, 
# así que aquí solo definimos las rutas limpias.
router = APIRouter()

# 2. Dependencia: Función para abrir y cerrar la conexión a la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 3. La Ruta Exclusiva del Administrador
@router.get("/pedidos/todos")
async def monitor_tiempo_real(db: Session = Depends(get_db)):
    """
    Panel del Administrador:
    Consulta la base de datos y devuelve absolutamente todos los pedidos 
    sin importar su estado, para verlos en tiempo real.
    """
    # Buscamos todos los registros en la tabla PedidoDB
    pedidos = db.query(models.PedidoDB).all()
    
    # Devolvemos un resumen y la lista completa
    return {
        "total_activos": len(pedidos), 
        "pedidos": pedidos
    }