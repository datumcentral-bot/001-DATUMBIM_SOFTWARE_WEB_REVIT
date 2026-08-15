from sqlalchemy import Column, String, DateTime, Text, Boolean, Integer, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datumbim.db.session import Base

class DesignView(Base):
    __tablename__ = "design_views"

    id = Column(String, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    view_type = Column(String(50), nullable=False)
    discipline = Column(String(50), nullable=False)
    visibility_state = Column(Boolean, default=True)
    active_state = Column(Boolean, default=False)
    camera_state = Column(Text, nullable=True)
    model_reference = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Element(Base):
    __tablename__ = "elements"

    id = Column(String, primary_key=True, index=True)
    type_id = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    name = Column(String(255), nullable=False)
    properties = Column(Text, nullable=True)
    transform_state = Column(Text, nullable=True)
    visibility = Column(Boolean, default=True)
    selection_state = Column(String(50), default="none")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    project_id = Column(String, ForeignKey("projects.id"), nullable=True)

class SelectionSet(Base):
    __tablename__ = "selection_sets"

    id = Column(String, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    element_ids = Column(Text, nullable=True)
    filter_criteria = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    project_id = Column(String, ForeignKey("projects.id"), nullable=True)
