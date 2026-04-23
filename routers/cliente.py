from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import SessionLocal

# 1. Creamos el "Departamento" del Cliente
router = APIRouter()

# 2. Dependencia de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 3. Ruta POST: El cliente crea un nuevo pedido
@router.post("/pedido/crear")
async def solicitar_delivery(datos: schemas.PedidoCrear, db: Session = Depends(get_db)):
    """
    El cliente o el restaurante envía los datos básicos.
    El sistema lo guarda como "Pendiente" y devuelve un número de ticket.
    """
    # Usamos **datos.model_dump() para convertir el esquema Pydantic a un diccionario 
    # y pasárselo a SQLAlchemy rápidamente
    nuevo_pedido = models.PedidoDB(**datos.model_dump())
    
    db.add(nuevo_pedido)
    db.commit()
    db.refresh(nuevo_pedido)
    
    return {
        "mensaje": "Pedido registrado. Buscando motorizado...", 
        "tu_numero_de_ticket": nuevo_pedido.id,
        "indicacion": "Guarda este número para rastrear tu pedido."
    }

# 4. Ruta GET: El cliente consulta el estado de su pedido
@router.get("/rastreo/{ticket_id}")
async def rastrear_pedido(ticket_id: int, db: Session = Depends(get_db)):
    """
    El cliente ingresa su ID para saber si ya lo recogieron, 
    cuánto le va a costar y en qué tiempo llega.
    """
    pedido = db.query(models.PedidoDB).filter(models.PedidoDB.id == ticket_id).first()
    
    # Validamos que el ticket exista
    if not pedido:
        raise HTTPException(status_code=404, detail="Ticket inválido o no existe")
    
    # Preparamos la respuesta básica
    respuesta = {
        "estado_actual": pedido.estado,
        "a_pagar_al_repartidor": f"S/ {pedido.total_a_cobrar}"
    }
    
    # Lógica de negocio: Si el pedido ya fue aceptado o está en camino,
    # le mostramos el tiempo estimado que puso el motorizado.
    if pedido.estado in ["Aceptado", "Recogido", "En Camino"]:
        respuesta["llegada_estimada"] = f"Aprox {pedido.tiempo_estimado_min} minutos"
        respuesta["info_adicional"] = "Por favor, ten el efectivo listo."
        
    return respuesta