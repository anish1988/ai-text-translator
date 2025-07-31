# services/history_service.py

from sqlalchemy.orm import Session
from models.db_models import TranslationHistory

class HistoryService:
    def __init__(self, db: Session):
        self.db = db
    
    def log(self, user_id: int, src: str, dest: str, original: str, translated: str):
        record = TranslationHistory(user_id= user_id, source_lang= src, target_lang= dest,
                                    original_text= original, translated_text= translated)
        self.db.add(record)
        self.db.commit()
        