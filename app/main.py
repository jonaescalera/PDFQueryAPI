from fastapi import FastAPI
from app.api.routers import resume

app = FastAPI(    
    title="Mi API",
    description="Descripción de mi API",
    version="0.1.0")

app.include_router(resume.router, prefix='/resume')
