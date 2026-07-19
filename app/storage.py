"""
Camada de acesso ao banco de dados (SQLite via SQLAlchemy).

Mantém as mesmas funções que o projeto já usava com o armazenamento em
memória (salvar_pedido, atualizar_status, buscar_pedido), só que agora
os dados ficam guardados de verdade no arquivo gateway.db e sobrevivem
a reinícios do servidor.
"""
from app.database import SessionLocal, engine, Base
from app.models import Pedido

# Cria a tabela "pedidos" no banco (gateway.db) se ela ainda não existir.
Base.metadata.create_all(bind=engine)


def salvar_pedido(pedido_id: str, dados: dict) -> None:
    db = SessionLocal()
    try:
        pedido = Pedido(
            pedido_id=pedido_id,
            preference_id=dados["preference_id"],
            status=dados.get("status", "pendente"),
            email_comprador=dados["email_comprador"],
        )
        db.add(pedido)
        db.commit()
    finally:
        db.close()


def atualizar_status(pedido_id: str, status: str) -> None:
    db = SessionLocal()
    try:
        pedido = db.query(Pedido).filter(Pedido.pedido_id == pedido_id).first()
        if pedido:
            pedido.status = status
            db.commit()
    finally:
        db.close()


def buscar_pedido(pedido_id: str) -> dict | None:
    db = SessionLocal()
    try:
        pedido = db.query(Pedido).filter(Pedido.pedido_id == pedido_id).first()
        if not pedido:
            return None
        return {
            "preference_id": pedido.preference_id,
            "status": pedido.status,
            "email_comprador": pedido.email_comprador,
        }
    finally:
        db.close()
