from sqlalchemy import Column, String, DateTime, Text, Boolean, Integer, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datumbim.db.session import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    file_path = Column(String(1024), nullable=True)
    file_format = Column(String(50), nullable=True)
    file_size = Column(Integer, nullable=True)
    version = Column(String(50), nullable=True)
    revision = Column(String(50), nullable=True)
    status = Column(String(50), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Level(Base):
    __tablename__ = "levels"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    name = Column(String(255), nullable=False)
    elevation = Column(Float, nullable=False, default=0.0)
    height = Column(Float, nullable=True)
    is_structural = Column(Boolean, default=False)
    is_ground = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Wall(Base):
    __tablename__ = "walls"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    level_id = Column(String, ForeignKey("levels.id"), nullable=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), default="Walls")
    type_id = Column(String(255), nullable=True)
    properties = Column(Text, nullable=True)
    transform_state = Column(Text, nullable=True)
    length = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    thickness = Column(Float, nullable=True)
    area = Column(Float, nullable=True)
    volume = Column(Float, nullable=True)
    visibility = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Door(Base):
    __tablename__ = "doors"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    level_id = Column(String, ForeignKey("levels.id"), nullable=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), default="Doors")
    type_id = Column(String(255), nullable=True)
    properties = Column(Text, nullable=True)
    transform_state = Column(Text, nullable=True)
    width = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    sill_height = Column(Float, nullable=True)
    head_height = Column(Float, nullable=True)
    visibility = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Window(Base):
    __tablename__ = "windows"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    level_id = Column(String, ForeignKey("levels.id"), nullable=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), default="Windows")
    type_id = Column(String(255), nullable=True)
    properties = Column(Text, nullable=True)
    transform_state = Column(Text, nullable=True)
    width = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    sill_height = Column(Float, nullable=True)
    head_height = Column(Float, nullable=True)
    visibility = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Roof(Base):
    __tablename__ = "roofs"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    level_id = Column(String, ForeignKey("levels.id"), nullable=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), default="Roofs")
    type_id = Column(String(255), nullable=True)
    properties = Column(Text, nullable=True)
    transform_state = Column(Text, nullable=True)
    area = Column(Float, nullable=True)
    slope = Column(Float, nullable=True)
    thickness = Column(Float, nullable=True)
    visibility = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Floor(Base):
    __tablename__ = "floors"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    level_id = Column(String, ForeignKey("levels.id"), nullable=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), default="Floors")
    type_id = Column(String(255), nullable=True)
    properties = Column(Text, nullable=True)
    transform_state = Column(Text, nullable=True)
    area = Column(Float, nullable=True)
    thickness = Column(Float, nullable=True)
    volume = Column(Float, nullable=True)
    visibility = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class StructuralColumn(Base):
    __tablename__ = "columns"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    level_id = Column(String, ForeignKey("levels.id"), nullable=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), default="Structural Columns")
    type_id = Column(String(255), nullable=True)
    properties = Column(Text, nullable=True)
    transform_state = Column(Text, nullable=True)
    base_level = Column(Float, nullable=True)
    top_level = Column(Float, nullable=True)
    length = Column(Float, nullable=True)
    cross_section_area = Column(Float, nullable=True)
    visibility = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Beam(Base):
    __tablename__ = "beams"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    level_id = Column(String, ForeignKey("levels.id"), nullable=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), default="Structural Framing")
    type_id = Column(String(255), nullable=True)
    properties = Column(Text, nullable=True)
    transform_state = Column(Text, nullable=True)
    length = Column(Float, nullable=True)
    cross_section_area = Column(Float, nullable=True)
    visibility = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Grid(Base):
    __tablename__ = "grids"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(String(50), default="line")
    direction = Column(String(50), nullable=True)
    properties = Column(Text, nullable=True)
    visibility = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Duct(Base):
    __tablename__ = "ducts"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    level_id = Column(String, ForeignKey("levels.id"), nullable=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), default="Ducts")
    type_id = Column(String(255), nullable=True)
    properties = Column(Text, nullable=True)
    transform_state = Column(Text, nullable=True)
    length = Column(Float, nullable=True)
    cross_section_area = Column(Float, nullable=True)
    visibility = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Pipe(Base):
    __tablename__ = "pipes"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    level_id = Column(String, ForeignKey("levels.id"), nullable=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), default="Pipes")
    type_id = Column(String(255), nullable=True)
    properties = Column(Text, nullable=True)
    transform_state = Column(Text, nullable=True)
    length = Column(Float, nullable=True)
    diameter = Column(Float, nullable=True)
    visibility = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class CableTray(Base):
    __tablename__ = "cable_trays"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    level_id = Column(String, ForeignKey("levels.id"), nullable=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), default="Cable Trays")
    type_id = Column(String(255), nullable=True)
    properties = Column(Text, nullable=True)
    transform_state = Column(Text, nullable=True)
    length = Column(Float, nullable=True)
    width = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    visibility = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Conduit(Base):
    __tablename__ = "conduits"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    level_id = Column(String, ForeignKey("levels.id"), nullable=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), default="Conduits")
    type_id = Column(String(255), nullable=True)
    properties = Column(Text, nullable=True)
    transform_state = Column(Text, nullable=True)
    length = Column(Float, nullable=True)
    diameter = Column(Float, nullable=True)
    visibility = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
