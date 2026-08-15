from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    is_active: Mapped[bool] = mapped_column(default=True)

class Model(Base):
    __tablename__ = "models"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    format: Mapped[str | None] = mapped_column(String(50))
    version: Mapped[str | None] = mapped_column(String(50))
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class Resource(Base):
    __tablename__ = "resources"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    path: Mapped[str] = mapped_column(String(1024), nullable=False, unique=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    extension: Mapped[str | None] = mapped_column(String(50))
    size: Mapped[int | None] = mapped_column(Integer)
    modified_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True))
    category: Mapped[str | None] = mapped_column(String(100))
    software: Mapped[str | None] = mapped_column(String(100))
    version: Mapped[str | None] = mapped_column(String(50))
    license: Mapped[str | None] = mapped_column(String(100))
    usability: Mapped[str | None] = mapped_column(String(50))
    is_duplicate: Mapped[bool] = mapped_column(default=False)
    project_relevance: Mapped[str | None] = mapped_column(String(50))
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
