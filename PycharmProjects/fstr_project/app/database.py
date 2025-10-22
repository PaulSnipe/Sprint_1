# app/database.py
import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- Найти .env, поднимаясь вверх от этого файла (app/) ---
def find_dotenv_upwards(filename=".env", max_levels=5):
    p = Path(__file__).resolve()
    for _ in range(max_levels):
        candidate = p.parent / filename
        if candidate.exists():
            return str(candidate)
        p = p.parent
    return None

dotenv_path = find_dotenv_upwards()
if dotenv_path:
    load_dotenv(dotenv_path)
    print(f"Loaded .env from: {dotenv_path}")
else:
    # Попытка просто load_dotenv() на случай, если процесс запускается из корня
    load_dotenv()
    print(".env not found by walking; attempted default load_dotenv(). If you rely on .env, place it in project root.")

# --- Получаем переменные окружения ---
DB_HOST = os.getenv("FSTR_DB_HOST")
DB_PORT = os.getenv("FSTR_DB_PORT")
DB_USER = os.getenv("FSTR_DB_LOGIN")
DB_PASS = os.getenv("FSTR_DB_PASS")
DB_NAME = os.getenv("FSTR_DB_NAME")

# --- Логируем (временно) что получили ---
print("DB ENV VARS (raw):")
print("  FSTR_DB_HOST:", DB_HOST)
print("  FSTR_DB_PORT:", DB_PORT)
print("  FSTR_DB_LOGIN:", DB_USER)
print("  FSTR_DB_PASS:", "<hidden>" if DB_PASS else None)
print("  FSTR_DB_NAME:", DB_NAME)

# --- Резервные (безопасные) значения и проверка ---
if DB_HOST is None:
    print("Warning: FSTR_DB_HOST not set; using 'localhost' as fallback.")
    DB_HOST = "localhost"

try:
    DB_PORT = int(DB_PORT) if DB_PORT is not None else 5432
except ValueError:
    print(f"Warning: FSTR_DB_PORT value is invalid ({os.getenv('FSTR_DB_PORT')}); using 5432.")
    DB_PORT = 5432

if DB_USER is None:
    print("Warning: FSTR_DB_LOGIN not set; using 'postgres' as fallback.")
    DB_USER = "postgres"

if DB_NAME is None:
    print("Warning: FSTR_DB_NAME not set; using 'fstr_db' as fallback.")
    DB_NAME = "fstr_db"

if DB_PASS is None:
    print("Warning: FSTR_DB_PASS not set; using empty password (may fail to connect).")
    DB_PASS = ""

# --- Собираем URL безопасно ---
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print("SQLALCHEMY_DATABASE_URL:", SQLALCHEMY_DATABASE_URL.replace(DB_PASS, "****" if DB_PASS else ""))

# --- Создаём engine и сессии ---
engine = create_engine(SQLALCHEMY_DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
Base = declarative_base()

# --- Зависимость для FastAPI ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
