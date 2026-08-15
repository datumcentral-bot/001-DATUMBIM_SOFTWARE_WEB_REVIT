from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from datumbim.routes.design import router as design_router

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

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "task": "000"}
