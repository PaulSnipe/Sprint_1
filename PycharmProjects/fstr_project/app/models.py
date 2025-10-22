# app/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    fam = Column(String, nullable=False)
    name = Column(String, nullable=False)
    otc = Column(String)
    phone = Column(String, nullable=False)

    passes = relationship("Pass", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"


class Coords(Base):
    __tablename__ = "coords"

    id = Column(Integer, primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    height = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Coords(lat={self.latitude}, lon={self.longitude}, h={self.height})>"


class Level(Base):
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True)
    winter = Column(String)
    summer = Column(String)
    autumn = Column(String)
    spring = Column(String)

    def __repr__(self):
        return f"<Level(id={self.id}, summer='{self.summer}', winter='{self.winter}')>"


class Pass(Base):
    __tablename__ = "passes"

    id = Column(Integer, primary_key=True)
    beauty_title = Column(String, nullable=False)
    title = Column(String, nullable=False)
    other_titles = Column(String)
    connect = Column(Text)
    add_time = Column(DateTime, server_default=func.now())
    status = Column(String, nullable=False, default="new")  # ← статус модерации

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    coords_id = Column(Integer, ForeignKey("coords.id"), nullable=False)
    level_id = Column(Integer, ForeignKey("levels.id"), nullable=False)

    user = relationship("User", back_populates="passes")
    coords = relationship("Coords")
    level = relationship("Level")
    images = relationship("Image", back_populates="pass_", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Pass(id={self.id}, title='{self.title}', status='{self.status}')>"


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    data = Column(Text, nullable=False)  # base64 изображение
    title = Column(String)
    pass_id = Column(Integer, ForeignKey("passes.id"), nullable=False)

    pass_ = relationship("Pass", back_populates="images")

    def __repr__(self):
        return f"<Image(id={self.id}, title='{self.title}')>"
