# Gateway de Pagamento — Mercado Pago + FastAPI

API em Python que integra com o Mercado Pago para criar cobranças (Pix, cartão,
boleto) e receber notificações automáticas de status via webhook.

## Como rodar

1. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure suas credenciais:**
   ```bash
   cp .env.example .env
   ```
   Edite o `.env` e coloque seu `MP_ACCESS_TOKEN` de teste, obtido em:
   https://www.mercadopago.com.br/developers/panel/app

3. **Rode o servidor:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

4. **Acesse a documentação interativa (Swagger):**
   http://localhost:8000/docs

## Testando o webhook localmente

O Mercado Pago precisa conseguir chamar sua rota `/webhook` pela internet.
Em desenvolvimento local, use o [ngrok](https://ngrok.com) para expor seu
servidor:

```bash
ngrok http 8000
```

Copie a URL gerada (ex: `https://abcd1234.ngrok.io/webhook`) e coloque no
`.env` em `WEBHOOK_URL`.

## Fluxo da aplicação

1. Seu frontend chama `POST /pagamentos` com os itens do pedido.
2. A API cria uma "preference" no Mercado Pago e devolve um `link_pagamento`.
3. Você redireciona o cliente para esse link — ele paga na página do Mercado Pago.
4. O Mercado Pago chama seu `POST /webhook` avisando quando o status mudar.
5. Você consulta `GET /pagamentos/{pedido_id}` para saber o status atual.

## Próximos passos sugeridos

- Trocar o armazenamento em memória (`app/storage.py`) por um banco de dados real.
- Validar a assinatura das notificações do webhook por segurança.
- Adicionar autenticação nas rotas da sua API.
- Criar testes automatizados usando o SDK em modo sandbox.
