from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# O banco vai ser um único arquivo chamado "gateway.db", criado
# automaticamente na mesma pasta do projeto na primeira vez que rodar.
DATABASE_URL = "sqlite:///./gateway.db"

engine = create_engine(
    DATABASE_URL,
    # Necessário apenas para SQLite: permite que o FastAPI acesse
    # o banco a partir de threads diferentes sem erro.
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Abre uma conexão com o banco e garante que ela é fechada no final."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
