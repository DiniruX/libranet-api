from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.actionLog import ActionLog
from app.schemas.actionLog import ActionLogCreate

def create_action_log(db: Session, action_log: ActionLogCreate):
    db_action_log = ActionLog(**action_log)
    db.add(db_action_log)
    db.commit()
    db.refresh(db_action_log)
    return db_action_log