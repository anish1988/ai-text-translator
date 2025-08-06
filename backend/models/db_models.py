# models/db_models.py
from sqlalchemy import Column, Integer, String, DateTime, func, Text
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

class LanguageTranslation(Base):
    __tablename__ = "vicidial_languages_pharases"  # match your actual MySQL table name

    id = Column(Integer, primary_key=True, index=True)
    language_id = Column(Integer)
    original_text = Column(Text)
    translated_text = Column(Text)
    created_at = Column(DateTime, server_default=func.now())