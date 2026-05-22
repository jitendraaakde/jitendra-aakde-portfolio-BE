from utils.groq import call_groq, call_docs_groq
from utils.openrouter import call_openrouter
from utils.logger import logger
from prompts import INTENT_IDENTIFICATION_PROMPT, GENERAL_QUERY_SYS_PROMPT, PDF_DOCUMENT_PROCESSING_PROMPT
from utils.pdf_extractor import extract_text_from_pdf
import re


def intent_identification(query: str) -> str:
    try:
        intent = call_groq(INTENT_IDENTIFICATION_PROMPT, [{"role": "user", "content": query}], temperature=0.2)

        if intent is None:
            logger.info("Groq failed for intent identification, trying OpenRouter fallback")
            intent = call_openrouter(INTENT_IDENTIFICATION_PROMPT, [{"role": "user", "content": query}], temperature=0.2)

        if intent is None:
            logger.warning("Both Groq and OpenRouter failed for intent identification, defaulting to 'general'")
            return "general"

        logger.info(f"Identified Intent: {intent}")
        return intent.strip().lower()
    except Exception as e:
        logger.error(f"Error in intent identification: {e}")
        return "general"


def process_general_intent(query: str, history: list = None) -> str:
    try:
        conversations = history if history else []
        response = call_groq(GENERAL_QUERY_SYS_PROMPT, conversations, temperature=0.7)

        if response is None:
            logger.info("Groq failed, trying OpenRouter fallback")
            response = call_openrouter(GENERAL_QUERY_SYS_PROMPT, conversations, temperature=0.7)

        if response is None:
            return "I'm having trouble connecting right now. Please try again in a moment."

        return response.strip()
    except Exception as e:
        logger.error(f"Error processing general intent: {e}")
        return None


def _extract_resume_contact(query: str, resume_text: str) -> str | None:
    lowered = query.lower()
    if "email" not in lowered and "mail" not in lowered and "contact" not in lowered:
        return None

    email_match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", resume_text or "")
    if email_match:
        return email_match.group(0)
    return None


def process_user_intent(query: str, history: list = None) -> str:
    try:
        history_context = ""
        if history and len(history) > 0:
            history_context = "\n\nPrevious conversation for context:\n"
            for msg in history[-6:]:
                role = "User" if msg["role"] == "user" else "Assistant"
                history_context += f"{role}: {msg['content']}\n"

        resume_text = extract_text_from_pdf("data/Jitendra_aakde_resume.pdf") or ""

        contact_email = _extract_resume_contact(query, resume_text)
        if contact_email:
            return contact_email

        if not resume_text.strip():
            logger.warning("Resume text could not be extracted; refusing to answer from missing source")
            return "I don't have that information here."

        prompt_with_context = PDF_DOCUMENT_PROCESSING_PROMPT.format(query=query) + history_context

        response = call_docs_groq(
            system_instructions=prompt_with_context,
            document_text=resume_text,
            temperature=0.1,
        )

        if response is None:
            logger.info("Groq docs failed, trying OpenRouter fallback for user intent")
            fallback_prompt = f"""{prompt_with_context}

Here is the resume/document content to reference:
---
{resume_text}
---

Based on the above document, answer the user's query. If the answer is not present, respond exactly: I don't have that information here."""
            response = call_openrouter(fallback_prompt, history if history else [], temperature=0.1)

        if response is None:
            return "I'm having trouble accessing my information right now. Please try again in a moment."

        return response.strip()
    except Exception as e:
        logger.error(f"Error processing user intent: {e}")
        return None


def process_chat_message(query: str, history: list) -> str:
    try:
        query_intent = intent_identification(query)

        if query_intent == "user":
            return process_user_intent(query, history)
        else:
            return process_general_intent(query, history)
    except Exception as e:
        logger.error(f"Error processing chat message: {e}")
        return "I'm sorry, something went wrong while processing your request."
