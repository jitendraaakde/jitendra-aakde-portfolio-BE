
from fastapi import APIRouter, HTTPException
from schemas import ChatRequest, ChatResponse
from utils.validate_message import preprocess_user_message
from utils.logger import logger
from services.chat_service import process_chat_message
from fastapi import status

router = APIRouter()

@router.post("/chat", status_code=status.HTTP_200_OK)
async def chat(payload: ChatRequest):
    try:
        query = preprocess_user_message(payload.message.strip())
        conversation_history = payload.conversation_history or []   
        conversation_history.append({"role": "user", "content": query})
        response = process_chat_message(query, conversation_history)
        # return ChatResponse(reply=response)
        conversation_history.append({"role": "assistant", "content": response})
        return {"reply": response, "conversation_history": conversation_history}
    except Exception as e:
        logger.error(f"Error processing chat: {e}")
        return HTTPException(status_code=500, detail="Internal Server Error")   