import requests
from config import Config
from utils.logger import logger


GROQ_API_KEY = Config.GROQ_API_KEY
GROQ_MODEL = Config.GROQ_MODEL
GROQ_BASE_URL = "https://api.groq.com/openai/v1/chat/completions"


def call_groq(system_instructions: str, user_conversations: list, temperature: float = 0.5) -> str | None:
    """
    Call Groq API using the llama-3.3-70b-versatile model.
    Uses OpenAI-compatible API format.
    """
    try:
        if not GROQ_API_KEY:
            logger.error("Groq API key not configured")
            return None
            
        logger.info("Calling Groq API")
        
        # Build messages in OpenAI format
        messages = [{"role": "system", "content": system_instructions}]
        
        for msg in user_conversations:
            role = msg["role"]
            # Convert "model" to "assistant" if needed
            if role == "model":
                role = "assistant"
            messages.append({"role": role, "content": msg["content"]})
        
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": GROQ_MODEL,
            "messages": messages,
            "temperature": temperature
        }
        
        logger.info(f"Groq Request: model={GROQ_MODEL}, messages_count={len(messages)}")
        
        response = requests.post(
            GROQ_BASE_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code != 200:
            logger.error(f"Groq API error: {response.status_code} - {response.text}")
            return None
        
        data = response.json()
        
        if "choices" not in data or len(data["choices"]) == 0:
            logger.warning("No choices in Groq response")
            return None
        
        response_text = data["choices"][0]["message"]["content"].strip()
        logger.info(f"Groq Response: {response_text}")
        
        return response_text
        
    except requests.exceptions.Timeout:
        logger.error("Groq API request timed out")
        return None
    except Exception as e:
        logger.error(f"Groq API error: {e}")
        return None


def call_docs_groq(system_instructions: str, document_text: str, temperature: float = 0.5) -> str | None:
    """
    Call Groq API with document text included in the prompt.
    Since Groq doesn't have native PDF support, we include the text in the prompt.
    """
    try:
        if not GROQ_API_KEY:
            logger.error("Groq API key not configured")
            return None
            
        logger.info("Calling Groq API with document context")
        
        # Include document content in the system prompt
        enhanced_prompt = f"""{system_instructions}

Here is the document content to reference:
---
{document_text}
---

Based on the above document, answer the user's query."""
        
        messages = [{"role": "system", "content": enhanced_prompt}]
        
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": GROQ_MODEL,
            "messages": messages,
            "temperature": temperature
        }
        
        logger.info(f"Groq Docs Request: model={GROQ_MODEL}")
        
        response = requests.post(
            GROQ_BASE_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code != 200:
            logger.error(f"Groq Docs API error: {response.status_code} - {response.text}")
            return None
        
        data = response.json()
        
        if "choices" not in data or len(data["choices"]) == 0:
            logger.warning("No choices in Groq docs response")
            return None
        
        response_text = data["choices"][0]["message"]["content"].strip()
        logger.info(f"Groq Docs Response: {response_text}")
        
        return response_text
        
    except requests.exceptions.Timeout:
        logger.error("Groq Docs API request timed out")
        return None
    except Exception as e:
        logger.error(f"Groq Docs API error: {e}")
        return None
