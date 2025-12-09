from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from services.tts_service import generate_speech
from utils.logger import logger

router = APIRouter()

class TTSRequest(BaseModel):
    text: str
    voice: str | None = None

class TTSResponse(BaseModel):
    audio: str
    format: str = "mp3"

@router.post("/tts", response_model=TTSResponse, status_code=status.HTTP_200_OK)
async def text_to_speech(payload: TTSRequest):
    """
    Convert text to speech using Unreal Speech API.
    Returns base64-encoded MP3 audio.
    """
    try:
        if not payload.text or not payload.text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text is required"
            )
        
        audio_base64 = generate_speech(
            text=payload.text.strip(),
            voice_id=payload.voice
        )
        
        if not audio_base64:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate speech"
            )
        
        return TTSResponse(audio=audio_base64, format="mp3")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"TTS endpoint error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
