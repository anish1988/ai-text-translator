# models/db_models.py
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TranslationHistory(Base):
    __tablename__ = "translation_history"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    source_lang = Column(String)
    target_lang = Column(String)
    original_text = Column(String)
    translated_text = Column(String)
    created_at = Column(DateTime, server_default=func.now())