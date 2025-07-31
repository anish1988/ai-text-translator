# File: backend/app.py
from fastapi import FastAPI
from routes import translate, upload, voice
from models.db_models import Base
from db import engine
import sys
import os
sys.path.append(os.path.dirname(__file__))

app = FastAPI()

app.include_router(translate.router)
app.include_router(upload.router)
app.include_router(voice.router)

Base.metadata.create_all(bind=engine)

#@app.get("/")
#def root():
 #   return {"message": "AI Translator Backend Running..."}