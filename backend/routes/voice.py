# routes/voice.py
from fastapi import APIRouter
from services.tts_service import GoogleTTSService
from fastapi.responses import StreamingResponse
from io import BytesIO

router = APIRouter(prefix="/voice", tags=["Voice"])

@router.post("/speak")
def speak(text: str):
    tts = GoogleTTSService()
    audio = tts.speak(text)
    return StreamingResponse(BytesIO(audio), media_type="audio/mpeg")
