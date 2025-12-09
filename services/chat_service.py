from utils.gemini import call_gemini, call_docs_gemini
from utils.logger import logger
from prompts import INTENT_IDENTIFICATION_PROMPT, GENERAL_QUERY_SYS_PROMPT, PDF_DOCUMENT_PROCESSING_PROMPT

def intent_identification(query: str) -> str:
    try:
        intent = call_gemini(INTENT_IDENTIFICATION_PROMPT, [{"role": "user", "content": query}], temperature=0.2)
        logger.info(f"Identified Intent: {intent}")
        return intent.strip().lower()
    except Exception as e:
        print(f"Error in intent identification: {e}")

def process_general_intent(query: str, history: list = None) -> str:
    try:
        # History already contains the user message from the controller
        conversations = history if history else []
        
        response = call_gemini(GENERAL_QUERY_SYS_PROMPT, conversations, temperature=0.7)
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
        
        response = call_docs_gemini(
            system_instructions=prompt_with_context,
            document_name="data/Jitendra_aakde_resume.pdf",
            temperature=0.3
        )
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