# routes/upload.py

from fastapi import APIRouter, UploadFile, File
from services.file_parser import FileParser
from services.openai_translator import LangChainTranslator

router = APIRouter(prefix="/upload", tags=["File Upload"])

@router.post("/file")
def upload(file: UploadFile = File(...)):
    path = f"/tmp/{file.filename}"
    with open(path, "wb") as f:
        f.write(file.file.read())
    
    lines = FileParser.extract_text_column(path)
    translator = LangChainTranslator()
    result = [translator.translate(line, "hi") for line in lines]  # Translate to Hindi for example
    return {"translations": result}