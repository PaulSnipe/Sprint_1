# app/routes/submit.py
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import PassRepository

router = APIRouter(prefix="", tags=["Submit Data"])


@router.post(
    "/submitData",
    status_code=status.HTTP_200_OK,
    summary="Добавление нового перевала",
    description="Принимает JSON с данными о перевале от туриста и сохраняет их в базу данных."
)
def submit_data(data: dict = Body(...), db: Session = Depends(get_db)):
    """
    Обрабатывает POST-запрос с данными о перевале.
    Проверяет наличие обязательных полей, сохраняет в базу и возвращает:
      - status: код операции (200, 400, 500)
      - message: текст ошибки или подтверждение
      - id: идентификатор созданной записи
    """

    required_fields = ["beauty_title", "title", "user", "coords", "level", "images"]
    missing_fields = [f for f in required_fields if f not in data]

    if missing_fields:
        return {
            "status": status.HTTP_400_BAD_REQUEST,
            "message": f"Отсутствуют обязательные поля: {', '.join(missing_fields)}",
            "id": None,
        }

    try:
        result = PassRepository.add_pass(db, data)
        return result

    except HTTPException as http_err:
        return {
            "status": http_err.status_code,
            "message": str(http_err.detail),
            "id": None,
        }

    except Exception as e:
        return {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"Ошибка на сервере: {str(e)}",
            "id": None,
        }
