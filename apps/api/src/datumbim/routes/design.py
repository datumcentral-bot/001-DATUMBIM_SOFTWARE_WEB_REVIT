from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/design", tags=["design"])

class DesignStatusResponse(BaseModel):
    status: str
    task: str
    engine: str

class ViewResponse(BaseModel):
    id: str
    name: str
    type: str
    discipline: str
    visibility_state: bool
    active_state: bool

@router.get("/status", response_model=DesignStatusResponse)
async def design_status() -> DesignStatusResponse:
    return DesignStatusResponse(status="ok", task="003", engine="design-engine-foundation")

@router.get("/views", response_model=list[ViewResponse])
async def list_views() -> list[ViewResponse]:
    return [
        ViewResponse(id="view-3d", name="{3D}", type="3d", discipline="generic", visibility_state=True, active_state=True),
        ViewResponse(id="floor-plan", name="Floor Plan", type="floor-plan", discipline="architecture", visibility_state=True, active_state=False),
    ]
