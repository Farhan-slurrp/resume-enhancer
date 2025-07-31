from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="Resume Enhancer Agent")
app.include_router(router)