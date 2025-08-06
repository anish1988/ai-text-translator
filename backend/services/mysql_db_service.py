from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.db_models import LanguageTranslation
from interfaces.database_interface import DatabaseInterface



class MySQLDBService(DatabaseInterface):
    def __init__(self, host, port, user, password, dbname):
        print (host)
        print (user)
        print (password)
        url = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{dbname}"
        self.engine = create_engine(url)
        self.Session = sessionmaker(bind=self.engine)

    def fetch_texts(self, language_id: int) -> list[str]:
        with self.Session() as session:
            rows = session.query(LanguageTranslation).filter_by(language_id=language_id).all()
            return [row.text for row in rows]

    def insert_translations(self, language_id: int, texts: list[str]):
        with self.Session() as session:
            for text in texts:
                entry = LanguageTranslation(language_id=language_id, text=text)
                session.add(entry)
            session.commit()
