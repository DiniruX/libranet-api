from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import test, library, user, book, reservation, interLibReservations, fine, search

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

app.include_router(test.router)
app.include_router(library.router)
app.include_router(user.router)
app.include_router(book.router)
app.include_router(reservation.router)
app.include_router(interLibReservations.router)
app.include_router(fine.router)
app.include_router(search.router)