from app.routers.certificates import router as certificates_router
from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routers.jobs import router as jobs_router

app = FastAPI(title="Bulk Certificate Generator")


@app.on_event("startup")
def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(jobs_router)
app.include_router(certificates_router)
