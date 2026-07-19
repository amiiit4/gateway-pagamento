from sqlalchemy import Column, String, DateTime, func
from app.database import Base


class Pedido(Base):
    """
    Representa a tabela 'pedidos' no banco. Cada linha é um pedido
    criado através da rota POST /pagamentos.
    """
    __tablename__ = "pedidos"

    pedido_id = Column(String, primary_key=True, index=True)
    preference_id = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pendente")
    email_comprador = Column(String, nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())
