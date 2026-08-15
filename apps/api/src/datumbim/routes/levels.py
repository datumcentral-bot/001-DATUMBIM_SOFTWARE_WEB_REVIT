from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datumbim.db.session import get_db
from datumbim.models.bim import Level, Wall, Door, Window, Roof, Floor, Column, Beam, Grid
from datumbim.schemas.level import LevelCreate, LevelUpdate, LevelResponse

router = APIRouter(prefix="/levels", tags=["levels"])


@router.get("/", response_model=list[LevelResponse])
async def list_levels(project_id: str = Query(...), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Level).where(Level.project_id == project_id).order_by(Level.elevation.asc()))
    return result.scalars().all()


@router.post("/", response_model=LevelResponse)
async def create_level(payload: LevelCreate, db: AsyncSession = Depends(get_db)):
    level = Level(**payload.model_dump())
    db.add(level)
    await db.commit()
    await db.refresh(level)
    return level


@router.get("/{level_id}", response_model=LevelResponse)
async def get_level(level_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Level).where(Level.id == level_id))
    level = result.scalar_one_or_none()
    if not level:
        raise HTTPException(status_code=404, detail="Level not found")
    return level


@router.put("/{level_id}", response_model=LevelResponse)
async def update_level(level_id: str, payload: LevelUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Level).where(Level.id == level_id))
    level = result.scalar_one_or_none()
    if not level:
        raise HTTPException(status_code=404, detail="Level not found")
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(level, key, value)
    await db.commit()
    await db.refresh(level)
    return level


@router.delete("/{level_id}")
async def delete_level(level_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Level).where(Level.id == level_id))
    level = result.scalar_one_or_none()
    if not level:
        raise HTTPException(status_code=404, detail="Level not found")
    await db.delete(level)
    await db.commit()
    return {"detail": "Level deleted"}
