from sqlalchemy import Column, Integer, String, Float
from database import Base

class PedidoDB(Base):
    __tablename__ = "pedidos"

    # El ID funcionará como nuestro "Ticket" para el cliente
    id = Column(Integer, primary_key=True, index=True)
    
    # Datos del Cliente y Ruta
    cliente_nombre = Column(String)
    direccion_recojo = Column(String)
    direccion_entrega = Column(String)
    total_a_cobrar = Column(Float)
    
    # Control de Estado
    # Estados válidos: Pendiente, Aceptado, Recogido, En Camino, Entregado, Cancelado
    estado = Column(String, default="Pendiente") 
    
    # Datos del Motorizado
    motorizado_id = Column(Integer, nullable=True) # Se llena cuando alguien acepta el pedido
    tiempo_estimado_min = Column(Integer, nullable=True) # Tiempo en minutos (ETA)