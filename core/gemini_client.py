import streamlit as st
from google import genai
from utils.logger import get_logger

logger = get_logger()

class GeminiClient:
    def __init__(self):
        api_key = st.secrets.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Gemini API Key missing")

        self.client = genai.Client(api_key=api_key)

        self.model_name = "gemini-3.1-flash-lite-preview"

    def generate_response(self, prompt: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text

        except Exception as e:
            logger.error(f"Gemini API Error: {str(e)}")
            return (
                "⚠️ Daily API quota reached or model unavailable."
            )
