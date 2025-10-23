# app/crud.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app import models


class PassRepository:
    @staticmethod
    def add_pass(db: Session, data: dict):
        try:
            user_data = data["user"]
            user = db.query(models.User).filter_by(email=user_data["email"]).first()
            if not user:
                user = models.User(**user_data)
                db.add(user)
                db.flush()

            coords = models.Coords(**data["coords"])
            db.add(coords)
            db.flush()

            level = models.Level(**data["level"])
            db.add(level)
            db.flush()

            new_pass = models.Pass(
                beauty_title=data.get("beauty_title"),
                title=data["title"],
                other_titles=data.get("other_titles"),
                connect=data.get("connect"),
                user_id=user.id,
                coords_id=coords.id,
                level_id=level.id,
            )
            db.add(new_pass)
            db.flush()

            for img in data["images"]:
                image = models.Image(data=img["data"], title=img.get("title"), pass_id=new_pass.id)
                db.add(image)

            db.commit()
            return {"status": 200, "message": None, "id": new_pass.id}

        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Ошибка базы данных: {e}")
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Неожиданная ошибка: {e}")

    @staticmethod
    def get_pass_by_id(db: Session, pass_id: int):
        record = db.query(models.Pass).filter(models.Pass.id == pass_id).first()
        if not record:
            raise HTTPException(status_code=404, detail="Перевал не найден")
        return {
            "id": record.id,
            "status": record.status,
            "beauty_title": record.beauty_title,
            "title": record.title,
            "other_titles": record.other_titles,
            "connect": record.connect,
            "add_time": record.add_time,
            "user": {
                "email": record.user.email,
                "fam": record.user.fam,
                "name": record.user.name,
                "otc": record.user.otc,
                "phone": record.user.phone,
            },
            "coords": {
                "latitude": record.coords.latitude,
                "longitude": record.coords.longitude,
                "height": record.coords.height,
            },
            "level": {
                "winter": record.level.winter,
                "summer": record.level.summer,
                "autumn": record.level.autumn,
                "spring": record.level.spring,
            },
            "images": [{"title": img.title, "data": img.data} for img in record.images],
        }

    @staticmethod
    def update_pass(db: Session, pass_id: int, new_data: dict):
        record = db.query(models.Pass).filter(models.Pass.id == pass_id).first()
        if not record:
            return {"state": 0, "message": "Перевал не найден"}
        if record.status != "new":
            return {"state": 0, "message": "Редактирование запрещено: статус не 'new'"}
        try:
            for field in ["beauty_title", "title", "other_titles", "connect"]:
                if field in new_data:
                    setattr(record, field, new_data[field])
            if "coords" in new_data:
                for k, v in new_data["coords"].items():
                    setattr(record.coords, k, v)
            if "level" in new_data:
                for k, v in new_data["level"].items():
                    setattr(record.level, k, v)
            db.commit()
            return {"state": 1, "message": "Запись успешно обновлена"}
        except Exception as e:
            db.rollback()
            return {"state": 0, "message": f"Ошибка при обновлении: {str(e)}"}

    @staticmethod
    def get_passes_by_email(db: Session, email: str):
        user = db.query(models.User).filter_by(email=email).first()
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        passes = db.query(models.Pass).filter_by(user_id=user.id).all()
        return [
            {"id": p.id, "title": p.title, "status": p.status, "add_time": p.add_time}
            for p in passes
        ]
