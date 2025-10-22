# app/main.py
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.database import Base, engine
from app.routes import submit

app = FastAPI(title="FSTR Pass Submission API")

# Регистрируем роутеры
app.include_router(submit.router)

# Событие при старте приложения
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    print(">>> MAIN.PY: СЕРВЕР ЗАПУСТИЛСЯ И БАЗА СОЗДАНА")

# Редирект с / на Swagger документацию
@app.get("/")
def root():
    return RedirectResponse(url="/docs")
