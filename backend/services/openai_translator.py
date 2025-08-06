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

    def translate(self, input_text: str, target_language: str) -> str:
       #prompt = ChatPromptTemplate.from_template("Translate this to {language} : {text}")
        prompt = ChatPromptTemplate.from_template(
                """
                You are an expert multilingual translator with deep understanding of cultural context and idiomatic expressions.

                Your task is to translate the following input into {target_language} as accurately and naturally as possible.

                - Detect the source language automatically if not explicitly English.
                - Preserve tone, context, and style (formal/informal) of the original.
                - Translate idioms and metaphors appropriately to match native fluency.
                - Return only the translated text in {target_language}, with no explanation or markup.

                Text: "{input_text}"
                """
            )
        chain = prompt | self.llm
        result = chain.invoke({"target_language": target_language, "input_text": input_text})
        return result.content.strip()
        

