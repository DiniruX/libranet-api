from fastapi import FastAPI
from app.api import test, library

app = FastAPI()
app.include_router(test.router)
app.include_router(library.router)