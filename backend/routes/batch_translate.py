from fastapi import APIRouter, Form
from services.openai_translator import LangChainTranslator
from services.mysql_db_service import MySQLDBService
from services.batch_translator_agent import BatchTranslatorAgent

router = APIRouter(prefix="/batch", tags=["Batch Translation"])

@router.post("/translate")
def run_batch_translation(
    source_lang_id: int = Form(...),
    target_lang_id: int = Form(...),
    target_language: str = Form(...),
    db_host: str = Form(None),
    db_port: int = Form(None),
    db_user: str = Form(None),
    db_pass: str = Form(None),
    db_name: str = Form(None),
):
    translator = LangChainTranslator()

    # Use DB if creds provided, else skip
    db_service = None
    if all([db_host, db_port, db_user, db_pass, db_name]):
        db_service = MySQLDBService(db_host, db_port, db_user, db_pass, db_name)

    agent = BatchTranslatorAgent(translator, db_service)
    result = agent.run(source_lang_id, target_lang_id, target_language)
    return result
