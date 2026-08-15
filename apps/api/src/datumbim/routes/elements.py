from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datumbim.db.session import get_db
from datumbim.models.DesignModel import Element
from datumbim.models.bim import Wall, Door, Window, Roof, Floor, Column, Beam, Grid, Duct, Pipe, CableTray, Conduit
from datumbim.schemas.element import ElementCreate, ElementUpdate, ElementResponse

router = APIRouter(prefix="/elements", tags=["elements"])


@router.get("/", response_model=list[ElementResponse])
async def list_elements(project_id: str = Query(...), category: str | None = None, db: AsyncSession = Depends(get_db)):
    query = select(Element).where(Element.project_id == project_id)
    if category:
        query = query.where(Element.category == category)
    result = await db.execute(query.order_by(Element.created_at.asc()))
    return result.scalars().all()


@router.post("/", response_model=ElementResponse)
async def create_element(payload: ElementCreate, db: AsyncSession = Depends(get_db)):
    element = Element(**payload.model_dump())
    db.add(element)
    await db.commit()
    await db.refresh(element)
    return element


@router.get("/{element_id}", response_model=ElementResponse)
async def get_element(element_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Element).where(Element.id == element_id))
    element = result.scalar_one_or_none()
    if not element:
        raise HTTPException(status_code=404, detail="Element not found")
    return element


@router.put("/{element_id}", response_model=ElementResponse)
async def update_element(element_id: str, payload: ElementUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Element).where(Element.id == element_id))
    element = result.scalar_one_or_none()
    if not element:
        raise HTTPException(status_code=404, detail="Element not found")
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(element, key, value)
    await db.commit()
    await db.refresh(element)
    return element


@router.delete("/{element_id}")
async def delete_element(element_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Element).where(Element.id == element_id))
    element = result.scalar_one_or_none()
    if not element:
        raise HTTPException(status_code=404, detail="Element not found")
    await db.delete(element)
    await db.commit()
    return {"detail": "Element deleted"}
