from pydantic import BaseModel, Field
from typing import Optional


class ItemPedido(BaseModel):
    titulo: str = Field(..., example="Camiseta Preta P")
    quantidade: int = Field(..., gt=0, example=1)
    preco_unitario: float = Field(..., gt=0, example=79.90)


class CriarPagamentoRequest(BaseModel):
    pedido_id: str = Field(..., example="pedido-0001")
    itens: list[ItemPedido]
    email_comprador: str = Field(..., example="cliente@email.com")
    nome_comprador: Optional[str] = Field(None, example="Maria Silva")


class CriarPagamentoResponse(BaseModel):
    pedido_id: str
    preference_id: str
    link_pagamento: str  # init_point — para onde o cliente é redirecionado
    link_pagamento_sandbox: Optional[str] = None
