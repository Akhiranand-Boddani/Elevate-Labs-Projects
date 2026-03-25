import streamlit as st
from mistralai.client import Mistral
from utils.logger import get_logger
from config.settings import MISTRAL_MODEL

logger = get_logger()

class MistralClient:
    def __init__(self):
        api_key = st.secrets.get("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("Mistral API Key missing")

        self.client = Mistral(api_key=api_key)
        self.model_name = MISTRAL_MODEL

    def generate_response_stream(self, messages: list):
        try:
            response_stream = self.client.chat.stream(
                model=self.model_name,
                messages=messages
            )
            for chunk in response_stream:
                if chunk.data.choices[0].delta.content is not None:
                    yield chunk.data.choices[0].delta.content

        except Exception as e:
            logger.error(f"Mistral API Error: {str(e)}")
            yield "\n\n⚠️ An error occurred while communicating with Mistral AI."
