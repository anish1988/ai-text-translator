# services/openai_translator.py

from interfaces.translator_interface import TranslatorInterface
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

class LangChainTranslator(TranslatorInterface):

    def __init__(self, model_name="gpt-4", temperature=0.3):
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            openai_api_key=os.getenv("OPENAI_API_KEY")  # pulled from environment
        )

    def translate(self, text: str, target_language: str) -> str:
        prompt = ChatPromptTemplate.from_template("Translate this to {language} : {text}")
        chain = prompt | self.llm
        result = chain.invoke({"language": target_language, "text": text})
        return result.content.strip()
        

