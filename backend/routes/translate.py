# routes/translate.py

from fastapi import APIRouter
from models.translation_models import TranslationRequest, TranslationResponse
from services.translation_service import TranslationServices
from services.openai_translator import LangChainTranslator

router = APIRouter(prefix="/translate", tags=["Translation"])

translator = LangChainTranslator()
service = TranslationServices(translator)


@router.post("/text", response_model=TranslationResponse)
def translate_text(request: TranslationRequest):
    result = service.handle_translation(request.text, request.target_language)
    return TranslationResponse(translation=result)