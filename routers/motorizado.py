from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import SessionLocal

# 1. Creamos el "Departamento" del Motorizado
router = APIRouter()

# 2. Dependencia de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 3. Ruta GET: El motorizado busca trabajo disponible
@router.get("/pedidos_disponibles")
async def ver_pedidos_pendientes(db: Session = Depends(get_db)):
    """
    Muestra únicamente los pedidos que nadie ha aceptado todavía.
    """
    # Filtramos la base de datos buscando el estado inicial
    pendientes = db.query(models.PedidoDB).filter(models.PedidoDB.estado == "Pendiente").all()
    
    # Si no hay nada, mandamos un mensaje amigable
    if not pendientes:
        return {"mensaje": "No hay pedidos pendientes en este momento."}
        
    return pendientes

# 4. Ruta PUT: El motorizado gestiona el viaje
@router.put("/pedido/{ticket_id}/actualizar")
async def gestionar_viaje(ticket_id: int, accion: schemas.ActualizarEstado, db: Session = Depends(get_db)):
    """
    El motorizado cambia el estado del viaje. 
    Ejemplo de flujo: Pendiente -> Aceptado -> Recogido -> En Camino -> Entregado.
    """
    # Buscamos el pedido
    pedido = db.query(models.PedidoDB).filter(models.PedidoDB.id == ticket_id).first()
    
    if not pedido:
        raise HTTPException(status_code=404, detail="El viaje especificado no existe.")
    
    # ⚠️ REGLA DE NEGOCIO: Evitar que dos motorizados acepten el mismo pedido
    if accion.nuevo_estado == "Aceptado" and pedido.estado != "Pendiente":
        raise HTTPException(
            status_code=400, 
            detail="¡Uy! Alguien más ya aceptó este pedido. Busca otro."
        )

    # Actualizamos el estado general
    pedido.estado = accion.nuevo_estado
    
    # Lógica específica: Si recién lo acepta, registramos quién es y cuánto tarda
    if accion.nuevo_estado == "Aceptado":
        # Aseguramos que envíe su ID y el tiempo
        if not accion.motorizado_id or not accion.tiempo_estimado_min:
            raise HTTPException(
                status_code=400, 
                detail="Para aceptar el pedido debes enviar tu motorizado_id y el tiempo_estimado_min."
            )
        pedido.motorizado_id = accion.motorizado_id
        pedido.tiempo_estimado_min = accion.tiempo_estimado_min

    # Guardamos los cambios
    db.commit()
    db.refresh(pedido)
    
    return {
        "mensaje": f"Has actualizado el pedido a: {pedido.estado}", 
        "viaje": pedido
    }