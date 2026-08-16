from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from datumbim.routes.design import router as design_router
from datumbim.routes.projects import router as projects_router
from datumbim.routes.documents import router as documents_router
from datumbim.routes.levels import router as levels_router
from datumbim.routes.elements import router as elements_router
from datumbim.routes.formats import router as formats_router
from datumbim.routes.files import router as files_router
from datumbim.routes.connectors import router as connectors_router
from datumbim.routes.sessions import router as sessions_router
from datumbim.routes.observation import router as observation_router
from datumbim.routes.control import router as control_router

app = FastAPI(
    title="DATUMBIM API",
    description="DATUMBIM Web Revit Backend",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(design_router)
app.include_router(projects_router)
app.include_router(documents_router)
app.include_router(levels_router)
app.include_router(elements_router)
app.include_router(formats_router)
app.include_router(files_router)
app.include_router(connectors_router)
app.include_router(sessions_router)
app.include_router(observation_router)
app.include_router(control_router)

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "task": "010"}
