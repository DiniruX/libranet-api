from fastapi import FastAPI
from app.api import test

app = FastAPI()
app.include_router(test.router)