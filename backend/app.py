# File: backend/app.py
from fastapi import FastAPI


app = FastAPI()



@app.get("/")
def root():
    return {"message": "AI Translator Backend Running..."}