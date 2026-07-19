import os
from dotenv import load_dotenv

load_dotenv()

MP_ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
SUCCESS_URL = os.getenv("SUCCESS_URL", "https://seu-site.com/pagamento/sucesso")
FAILURE_URL = os.getenv("FAILURE_URL", "https://seu-site.com/pagamento/falha")
PENDING_URL = os.getenv("PENDING_URL", "https://seu-site.com/pagamento/pendente")

if not MP_ACCESS_TOKEN:
    raise RuntimeError(
        "MP_ACCESS_TOKEN não configurado. Copie .env.example para .env e preencha suas credenciais."
    )
