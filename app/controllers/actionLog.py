import os
import logging
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.actionLog import ActionLog
from app.schemas.actionLog import ActionLogCreate

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "action_logs.log")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def create_action_log(db: Session, action_log: ActionLogCreate):
    db_action_log = ActionLog(**action_log)
    db.add(db_action_log)
    db.commit()
    db.refresh(db_action_log)

    logging.info(
        f"action={action_log}"
    )
    return db_action_log