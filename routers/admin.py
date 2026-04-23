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

# routers/admin.py (Añadir al final)

@router.get("/liquidacion")
async def liquidacion_cierre(db: Session = Depends(get_db)):
    """
    Calcula cuánto dinero tiene cada motorizado en el bolsillo 
    y cuánto entró por Yape/Plin de los pedidos finalizados.
    """
    # 1. Traemos SOLO los pedidos que ya fueron entregados
    pedidos_entregados = db.query(models.PedidoDB).filter(models.PedidoDB.estado == "Entregado").all()
    
    # 2. Diccionario para agrupar las cuentas por motorizado
    cuadre = {}
    
    for pedido in pedidos_entregados:
        m_id = pedido.motorizado_id
        
        # Si es la primera vez que vemos a este motorizado en el bucle, le creamos su "boleta"
        if m_id not in cuadre:
            cuadre[m_id] = {
                "motorizado_id": m_id,
                "total_viajes": 0,
                "efectivo_en_mano": 0.0,
                "yape_plin_cuenta": 0.0,
                "total_general": 0.0
            }
            
        # 3. Sumamos el viaje
        cuadre[m_id]["total_viajes"] += 1
        cuadre[m_id]["total_general"] += pedido.total_a_cobrar
        
        # 4. Filtramos el dinero según el método de pago
        metodo = pedido.metodo_pago.lower()
        if "yape" in metodo or "plin" in metodo or "transferencia" in metodo:
            cuadre[m_id]["yape_plin_cuenta"] += pedido.total_a_cobrar
        else:
            cuadre[m_id]["efectivo_en_mano"] += pedido.total_a_cobrar
            
    # Convertimos el diccionario a una lista para enviarlo al frontend
    return list(cuadre.values())