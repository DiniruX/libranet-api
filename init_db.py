# init_db.py
from app.core.database import Base, engine
from app.models import library, user

Base.metadata.create_all(bind=engine)