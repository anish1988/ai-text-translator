from interfaces.translator_interface import TranslatorInterface


class TranslationServices:
    def __init__(self, translator: TranslatorInterface):
        self.translator = translator

    def handle_translation(self , text: str, target_language: str) -> str:
        return self.translator.translate(text, target_language)