# app/routes/submit.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import PassRepository

router = APIRouter(prefix="", tags=["Submit Data"])


@router.post("/submitData")
def submit_data(data: dict, db: Session = Depends(get_db)):
    """Добавление новой записи (перевала)"""
    required_fields = ["beauty_title", "title", "user", "coords", "level", "images"]
    missing_fields = [f for f in required_fields if f not in data]

    if missing_fields:
        return {
            "status": 400,
            "message": f"Отсутствуют обязательные поля: {', '.join(missing_fields)}",
            "id": None,
        }

    try:
        result = PassRepository.add_pass(db, data)
        return result
    except Exception as e:
        return {"status": 500, "message": f"Ошибка на сервере: {e}", "id": None}


@router.get("/submitData/{pass_id}")
def get_pass(pass_id: int, db: Session = Depends(get_db)):
    """Получить одну запись по ID"""
    return PassRepository.get_pass_by_id(db, pass_id)


@router.patch("/submitData/{pass_id}")
def update_pass(pass_id: int, data: dict, db: Session = Depends(get_db)):
    """Редактировать запись, если статус = 'new'"""
    return PassRepository.update_pass(db, pass_id, data)


@router.get("/submitData/")
def get_passes_by_user(user__email: str = Query(...), db: Session = Depends(get_db)):
    """Получить все перевалы пользователя по email"""
    return PassRepository.get_passes_by_email(db, user__email)
