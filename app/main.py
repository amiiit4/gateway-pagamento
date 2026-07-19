from fastapi import FastAPI, HTTPException, Request
from app.schemas import CriarPagamentoRequest, CriarPagamentoResponse
from app.mercado_pago_client import criar_preferencia, buscar_pagamento
from app import storage

app = FastAPI(title="Gateway de Pagamento (Mercado Pago)")


@app.post("/pagamentos", response_model=CriarPagamentoResponse)
def criar_pagamento(dados: CriarPagamentoRequest):
    """
    Cria um novo pagamento para um pedido.
    Retorna o link de checkout para redirecionar o cliente.
    """
    if storage.buscar_pedido(dados.pedido_id):
        raise HTTPException(status_code=400, detail="Esse pedido_id já foi usado.")

    preferencia = criar_preferencia(dados)

    storage.salvar_pedido(
        dados.pedido_id,
        {
            "preference_id": preferencia["id"],
            "status": "pendente",
            "email_comprador": dados.email_comprador,
        },
    )

    return CriarPagamentoResponse(
        pedido_id=dados.pedido_id,
        preference_id=preferencia["id"],
        link_pagamento=preferencia["init_point"],
        link_pagamento_sandbox=preferencia.get("sandbox_init_point"),
    )


@app.post("/webhook")
async def webhook(request: Request):
    """
    Endpoint chamado automaticamente pelo Mercado Pago quando o status
    de um pagamento muda (aprovado, recusado, estornado, etc).

    Documentação: https://www.mercadopago.com.br/developers/pt/docs/checkout-pro/additional-content/notifications/webhooks
    """
    corpo = await request.json()

    tipo = corpo.get("type")
    if tipo != "payment":
        # Ignora notificações que não são de pagamento (ex: merchant_order)
        return {"status": "ignorado"}

    payment_id = corpo.get("data", {}).get("id")
    if not payment_id:
        raise HTTPException(status_code=400, detail="ID do pagamento ausente na notificação.")

    pagamento = buscar_pagamento(payment_id)
    pedido_id = pagamento.get("external_reference")
    status_pagamento = pagamento.get("status")  # approved, pending, rejected, refunded, etc

    if pedido_id:
        storage.atualizar_status(pedido_id, status_pagamento)
        # Aqui você dispararia sua lógica de negócio:
        # - liberar acesso ao produto
        # - enviar e-mail de confirmação
        # - atualizar estoque
        # etc.

    return {"status": "recebido"}


@app.get("/pagamentos/{pedido_id}")
def consultar_status(pedido_id: str):
    """Consulta o status atual de um pedido."""
    pedido = storage.buscar_pedido(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    return pedido


@app.get("/")
def raiz():
    return {"status": "ok", "servico": "gateway de pagamento com Mercado Pago"}
