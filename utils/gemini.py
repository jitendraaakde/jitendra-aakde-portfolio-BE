import pathlib

from google import genai
from google.genai import types
from config import Config
from utils.logger import logger

GEMINI_API_KEY =  Config.GEMINI_API_KEY
client = genai.Client(api_key=GEMINI_API_KEY)

def call_gemini(system_instructions, user_conversations, temperature = 0.5, response_format=None):

    try:
        logger.info("Extracting System and User messages for Gemini")

        config_kwargs = {"system_instruction": system_instructions, "temperature": temperature}

        if response_format:
            config_kwargs["response_mime_type"] = "application/json"
            config_kwargs["response_schema"] = response_format

        config = types.GenerateContentConfig(**config_kwargs)

        user_messages = []
        
        for msg in user_conversations:

            if msg["role"] == "user":
                user_messages.append(
                    types.Content(
                        role="user",
                        parts=[types.Part.from_text(text=msg["content"])]
                    )
                )
            elif msg["role"] == "assistant":
                user_messages.append(
                    types.Content(
                        role="model",
                        parts=[types.Part.from_text(text=msg["content"])]
                    )
                )
        
        logger.info(f"Extraction complete for gemini")

        return call_gemini_api(config, user_messages)
    
    except Exception as e:
        logger.error(f"Error extracting messages for Gemini: {e}")
        return None

def call_gemini_api(config, messages):
    try:
        logger.info(f"Calling Gemini API")
        logger.info(f"Gemini Config: {config}")
        logger.info(f"Gemini User Messages: {messages}")
        
        response = client.models.generate_content(
            model=Config.GEMINI_MODEL_NAME,
            contents=messages,
            config=config
        )

        if not response.text:
            logger.warning("Received an empty response from Gemini API.")
            return None

        response_text = response.text.strip()

        logger.info(f"Gemini Response::  {response_text}")

        return response_text

    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return None

def call_docs_gemini(system_instructions, document_name, temperature=0.5):
    try:
        logger.info("Extracting System and User messages for Docs Gemini")

        filepath = pathlib.Path(document_name)

        config = types.GenerateContentConfig(temperature=temperature)

        response = client.models.generate_content(
            model=Config.GEMINI_MODEL_NAME,
            contents=[
                types.Part.from_bytes(
                    data=filepath.read_bytes(),
                    mime_type="application/pdf",
                ),
                system_instructions
            ],
            config=config
        )

        logger.info(f"Raw Gemini Response: {response}")

        result = ""
        if response and response.candidates:
            for part in response.candidates[0].content.parts:
                if hasattr(part, "text") and part.text:
                    result += part.text.strip() + "\n"

        if not result:
            logger.warning("No readable text found in Gemini response.")
            return None

        logger.info(f"Gemini Parsed Response: {result.strip()}")
        return result.strip()

    except Exception as e:
        logger.error(f"Error extracting messages for Docs Gemini: {e}")
        return None
