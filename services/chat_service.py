from utils.gemini import call_gemini, call_docs_gemini
from utils.openrouter import call_openrouter
from utils.logger import logger
from prompts import INTENT_IDENTIFICATION_PROMPT, GENERAL_QUERY_SYS_PROMPT, PDF_DOCUMENT_PROCESSING_PROMPT

def intent_identification(query: str) -> str:
    try:
        intent = call_gemini(INTENT_IDENTIFICATION_PROMPT, [{"role": "user", "content": query}], temperature=0.2)
        
        # Fallback to OpenRouter if Gemini fails
        if intent is None:
            logger.info("Gemini failed for intent identification, trying OpenRouter fallback")
            intent = call_openrouter(INTENT_IDENTIFICATION_PROMPT, [{"role": "user", "content": query}], temperature=0.2)
        
        if intent is None:
            logger.warning("Both Gemini and OpenRouter failed for intent identification, defaulting to 'general'")
            return "general"
            
        logger.info(f"Identified Intent: {intent}")
        return intent.strip().lower()
    except Exception as e:
        logger.error(f"Error in intent identification: {e}")
        return "general"  # Default to general on error

def process_general_intent(query: str, history: list = None) -> str:
    try:
        # History already contains the user message from the controller
        conversations = history if history else []
        
        # Try Gemini first
        response = call_gemini(GENERAL_QUERY_SYS_PROMPT, conversations, temperature=0.7)
        
        # Fallback to OpenRouter if Gemini fails
        if response is None:
            logger.info("Gemini failed, trying OpenRouter fallback")
            response = call_openrouter(GENERAL_QUERY_SYS_PROMPT, conversations, temperature=0.7)
        
        if response is None:
            return "I'm having trouble connecting right now. Please try again in a moment."
            
        return response.strip()
    except Exception as e:
        logger.error(f"Error processing general intent: {e}")
        return None

def process_user_intent(query: str, history: list = None) -> str:
    try:
        # Include conversation history context in the prompt
        history_context = ""
        if history and len(history) > 0:
            history_context = "\n\nPrevious conversation for context:\n"
            for msg in history[-6:]:  # Last 6 messages for context
                role = "User" if msg["role"] == "user" else "Assistant"
                history_context += f"{role}: {msg['content']}\n"
        
        prompt_with_context = PDF_DOCUMENT_PROCESSING_PROMPT.format(query=query) + history_context
        
        # Try Gemini first (with PDF document)
        response = call_docs_gemini(
            system_instructions=prompt_with_context,
            document_name="data/Jitendra_aakde_resume.pdf",
            temperature=0.3
        )
        
        # Fallback to OpenRouter if Gemini fails - include PDF text in prompt
        if response is None:
            logger.info("Gemini docs failed, trying OpenRouter fallback for user intent")
            
            # Extract text from resume PDF for OpenRouter
            from utils.pdf_extractor import extract_text_from_pdf
            resume_text = extract_text_from_pdf("data/Jitendra_aakde_resume.pdf")
            
            if resume_text:
                # Include resume content in the system prompt
                fallback_prompt = f"""{prompt_with_context}

Here is the resume/document content to reference:
---
{resume_text}
---

Based on the above document, answer the user's query."""
                response = call_openrouter(fallback_prompt, history if history else [], temperature=0.3)
            else:
                # No PDF text available, try with just the prompt
                response = call_openrouter(prompt_with_context, history if history else [], temperature=0.3)
        
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