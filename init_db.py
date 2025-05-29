# init_db.py
from app.core.database import Base, engine
from app.models import library, user, book

Base.metadata.create_all(bind=engine)