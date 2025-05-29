from fastapi import FastAPI
from app.api import test, library, user

app = FastAPI()
app.include_router(test.router)
app.include_router(library.router)
app.include_router(user.router)