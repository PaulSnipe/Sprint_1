# app/crud.py
from sqlalchemy.orm import Session
from app import models


class PassRepository:
    @staticmethod
    def add_pass(db: Session, data):
        try:
            user_data = data["user"]
            coords_data = data["coords"]
            level_data = data["level"]
            images_data = data["images"]

            user = db.query(models.User).filter_by(email=user_data["email"]).first()
            if not user:
                user = models.User(**user_data)
                db.add(user)
                db.flush()

            coords = models.Coords(**coords_data)
            level = models.Level(**level_data)

            new_pass = models.Pass(
                beauty_title=data["beauty_title"],
                title=data["title"],
                other_titles=data["other_titles"],
                connect=data["connect"],
                user=user,
                coords=coords,
                level=level,
            )
            db.add(coords)
            db.add(level)
            db.add(new_pass)
            db.flush()

            for img in images_data:
                image = models.Image(data=img["data"], title=img["title"], pass_id=new_pass.id)
                db.add(image)

            db.commit()
            return {"status": 200, "message": None, "id": new_pass.id}

        except Exception as e:
            db.rollback()
            return {"status": 500, "message": str(e), "id": None}
