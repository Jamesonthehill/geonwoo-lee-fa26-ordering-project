import os
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import conf


SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    (
        f"mysql+pymysql://{conf.user}:{quote_plus(conf.password)}"
        f"@{conf.host}:{conf.port}/{conf.database}?charset=utf8mb4"
    ),
)

connect_args = (
    {"check_same_thread": False}
    if SQLALCHEMY_DATABASE_URL.startswith("sqlite")
    else {}
)
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
