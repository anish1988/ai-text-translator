class BatchTranslatorAgent:
    def __init__(self, translator, db=None):
        self.translator = translator
        self.db = db

    def run(self, source_lang_id: int, target_lang_id: int, target_language: str):
        if not self.db:
            raise Exception("❌ No DB service provided")

        originals = self.db.fetch_texts(source_lang_id)
        errors, translated = [], []

        for idx, text in enumerate(originals, 1):
            try:
                result = self.translator.translate(text, target_language)
                translated.append(result)
            except Exception as e:
                errors.append({"index": idx, "text": text, "error": str(e)})

        self.db.insert_translations(target_lang_id, translated)

        return {"total": len(originals), "translated": len(translated), "errors": errors}
