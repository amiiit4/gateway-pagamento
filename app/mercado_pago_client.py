import mercadopago
from app.config import (
    MP_ACCESS_TOKEN,
    WEBHOOK_URL,
    SUCCESS_URL,
    FAILURE_URL,
    PENDING_URL,
)
from app.schemas import CriarPagamentoRequest

sdk = mercadopago.SDK(MP_ACCESS_TOKEN)


def criar_preferencia(dados: CriarPagamentoRequest) -> dict:
    """
    Cria uma 'preference' no Mercado Pago — isso gera o link de checkout
    para onde o cliente é redirecionado para pagar (Pix, cartão, boleto, etc).
    """
    itens_mp = [
        {
            "title": item.titulo,
            "quantity": item.quantidade,
            "unit_price": item.preco_unitario,
            "currency_id": "BRL",
        }
        for item in dados.itens
    ]

    preference_data = {
        "items": itens_mp,
        "payer": {"email": dados.email_comprador},
        "external_reference": dados.pedido_id,  # liga o pagamento ao seu pedido interno
        "back_urls": {
            "success": SUCCESS_URL,
            "failure": FAILURE_URL,
            "pending": PENDING_URL,
        },
        "auto_return": "approved",
        "notification_url": WEBHOOK_URL,  # o Mercado Pago vai chamar essa URL nas mudanças de status
    }

    resultado = sdk.preference().create(preference_data)
    return resultado["response"]


def buscar_pagamento(payment_id: str) -> dict:
    """Consulta os detalhes e o status atual de um pagamento pelo seu ID."""
    resultado = sdk.payment().get(payment_id)
    return resultado["response"]
