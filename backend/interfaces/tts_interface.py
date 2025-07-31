# interfaces/tts_interface.py
from abc import ABC, abstractmethod

class TextToSpeechInterface(ABC):
    @abstractmethod
    def speak(self, text: str) -> bytes:
        pass