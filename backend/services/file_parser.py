# services/file_parser.py
import pandas as pd

class FileParser:
    @staticmethod
    def extract_text_column(file_path: str) -> list[str]:
        df = pd.read_csv(file_path) if file_path.endswith(".csv") else pd.read_excel(file_path)
        return df.iloc[:, 0].dropna().tolist()