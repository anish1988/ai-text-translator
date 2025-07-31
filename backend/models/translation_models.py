# models/translation_models.py
from pydantic import BaseModel,Field

class TranslationRequest(BaseModel):
    text: str = Field(..., example="Hello, how are you?")
    target_language: str = Field(..., example="fr")

class TranslationResponse(BaseModel):
    translation: str = Field(..., example="Bonjour, comment ça va?")