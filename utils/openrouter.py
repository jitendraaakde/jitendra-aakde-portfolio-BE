import requests
from config import Config
from utils.logger import logger


OPENROUTER_API_KEY = Config.OPENROUTER_API_KEY
OPENROUTER_MODEL = Config.OPENROUTER_MODEL
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"


def call_openrouter(system_instructions: str, user_conversations: list, temperature: float = 0.5) -> str | None:
    """
    Call OpenRouter API as fallback when Gemini fails.
    Uses OpenAI-compatible API format.
    """
    try:
        if not OPENROUTER_API_KEY:
            logger.error("OpenRouter API key not configured")
            return None
            
        logger.info("Calling OpenRouter API as fallback")
        
        # Build messages in OpenAI format
        messages = [{"role": "system", "content": system_instructions}]
        
        for msg in user_conversations:
            role = msg["role"]
            # OpenRouter uses "assistant" not "model"
            if role == "model":
                role = "assistant"
            messages.append({"role": role, "content": msg["content"]})
        
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": Config.get_config_value("SITE_URL", "https://jitendra-aakde.dev"),
            "X-Title": "Jitendra Aakde Portfolio"
        }
        
        payload = {
            "model": OPENROUTER_MODEL,
            "messages": messages,
            "temperature": temperature
        }
        
        logger.info(f"OpenRouter Request: model={OPENROUTER_MODEL}, messages_count={len(messages)}")
        
        response = requests.post(
            OPENROUTER_BASE_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code != 200:
            logger.error(f"OpenRouter API error: {response.status_code} - {response.text}")
            return None
        
        data = response.json()
        
        if "choices" not in data or len(data["choices"]) == 0:
            logger.warning("No choices in OpenRouter response")
            return None
        
        response_text = data["choices"][0]["message"]["content"].strip()
        logger.info(f"OpenRouter Response: {response_text}")
        
        return response_text
        
    except requests.exceptions.Timeout:
        logger.error("OpenRouter API request timed out")
        return None
    except Exception as e:
        logger.error(f"OpenRouter API error: {e}")
        return None
