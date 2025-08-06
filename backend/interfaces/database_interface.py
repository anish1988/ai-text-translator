from abc import ABC, abstractmethod

class DatabaseInterface(ABC):
    @abstractmethod
    def fetch_texts(self, language_id: int) -> list[str]:
        pass

    @abstractmethod
    def insert_translations(self, language_id: int, texts: list[str]):
        pass
