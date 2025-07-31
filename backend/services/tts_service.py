# services/tts_service.py
from interfaces.tts_interface import TextToSpeechInterface
from gtts import gTTS
from io import BytesIO

class GoogleTTSService(TextToSpeechInterface):
    def speak(self, text: str) -> bytes:
        tts = gTTS(text)
        buffer = BytesIO()
        tts.write_to_fp(buffer)
        buffer.seek(0)
        return buffer.read()