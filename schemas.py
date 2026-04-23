from pydantic import BaseModel
from typing import Optional

# Lo que el cliente o restaurante envía para crear el pedido
class PedidoCrear(BaseModel):
    cliente_nombre: str
    direccion_recojo: str
    direccion_entrega: str
    total_a_cobrar: float

# Lo que el motorizado envía cuando cambia el estado de su viaje
class ActualizarEstado(BaseModel):
    nuevo_estado: str
    # Si acepta el pedido, debe calcular y enviar en cuántos minutos llega
    tiempo_estimado_min: Optional[int] = None 
    motorizado_id: Optional[int] = None