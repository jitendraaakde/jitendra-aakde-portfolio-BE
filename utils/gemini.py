import pathlib

from google import genai
from google.genai import types
from config import Config
from utils.logger import logger


def _create_gemini_client(api_key: str):
    """Create a Gemini client with the given API key."""
    return genai.Client(api_key=api_key)


def _call_gemini_api_with_client(client, config, messages):
    """Internal function to call Gemini API with a specific client."""
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
    logger.info(f"Gemini Response:: {response_text}")
    return response_text


def _call_gemini_with_fallback(config, messages):
    """
    Try Gemini API with each API key until one succeeds.
    Returns response text on success, None if all keys fail.
    """
    api_keys = Config.get_gemini_api_keys()
    
    if not api_keys:
        logger.error("No Gemini API keys configured")
        return None
    
    for i, api_key in enumerate(api_keys, 1):
        try:
            logger.info(f"Trying Gemini API with key {i} of {len(api_keys)}")
            client = _create_gemini_client(api_key)
            result = _call_gemini_api_with_client(client, config, messages)
            if result is not None:
                logger.info(f"Gemini API call succeeded with key {i}")
                return result
            else:
                logger.warning(f"Gemini API key {i} returned empty response, trying next key")
        except Exception as e:
            logger.warning(f"Gemini API key {i} failed: {e}")
    
    logger.error("All Gemini API keys exhausted, returning None for OpenRouter fallback")
    return None


def _call_docs_gemini_with_fallback(system_instructions, filepath, temperature):
    """
    Try Gemini Docs API with each API key until one succeeds.
    Returns response text on success, None if all keys fail.
    """
    api_keys = Config.get_gemini_api_keys()
    
    if not api_keys:
        logger.error("No Gemini API keys configured")
        return None
    
    config = types.GenerateContentConfig(temperature=temperature)
    
    for i, api_key in enumerate(api_keys, 1):
        try:
            logger.info(f"Trying Gemini Docs API with key {i} of {len(api_keys)}")
            client = _create_gemini_client(api_key)
            
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
            
            if result:
                logger.info(f"Gemini Docs API call succeeded with key {i}")
                logger.info(f"Gemini Parsed Response: {result.strip()}")
                return result.strip()
            else:
                logger.warning(f"Gemini Docs API key {i} returned empty response, trying next key")
                
        except Exception as e:
            logger.warning(f"Gemini Docs API key {i} failed: {e}")
    
    logger.error("All Gemini API keys exhausted for docs, returning None for OpenRouter fallback")
    return None


def call_gemini(system_instructions, user_conversations, temperature=0.5, response_format=None):
    """
    Call Gemini API with automatic fallback through multiple API keys.
    If all keys fail, returns None (caller should handle OpenRouter fallback).
    """
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

        return _call_gemini_with_fallback(config, user_messages)
    
    except Exception as e:
        logger.error(f"Error extracting messages for Gemini: {e}")
        return None


def call_docs_gemini(system_instructions, document_name, temperature=0.5):
    """
    Call Gemini Docs API with automatic fallback through multiple API keys.
    If all keys fail, returns None (caller should handle OpenRouter fallback).
    """
    try:
        logger.info("Extracting System and User messages for Docs Gemini")
        filepath = pathlib.Path(document_name)
        return _call_docs_gemini_with_fallback(system_instructions, filepath, temperature)
    except Exception as e:
        logger.error(f"Error extracting messages for Docs Gemini: {e}")
        return None
