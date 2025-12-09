import base64
import requests
from config import Config
from utils.logger import logger

def generate_speech(text: str, voice_id: str = None) -> str:
    """
    Generate speech audio from text using Unreal Speech API.
    Uses the /stream endpoint for fastest response (~300ms).
    
    Args:
        text: The text to convert to speech (max 1000 chars for stream)
        voice_id: Voice ID (Dan, Will, Scarlett, Liv, Amy)
    
    Returns:
        Base64-encoded MP3 audio string
    """
    try:
        if not text or not text.strip():
            logger.warning("Empty text provided for TTS")
            return None
        
        # Truncate to 1000 chars for stream endpoint
        if len(text) > 1000:
            text = text[:1000]
            logger.info(f"Truncated text to 1000 chars for Unreal Speech stream")
        
        voice = voice_id or Config.UNREAL_SPEECH_VOICE
        logger.info(f"Generating TTS with Unreal Speech voice: {voice}")
        
        # Use the /stream endpoint for fastest response
        response = requests.post(
            "https://api.v7.unrealspeech.com/stream",
            headers={
                "Authorization": f"Bearer {Config.UNREAL_SPEECH_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "Text": text,
                "VoiceId": voice,
                "Bitrate": "192k",
                "Speed": 0.2,
                "Pitch": 0.92
            }
        )
        
        if response.status_code != 200:
            logger.error(f"Unreal Speech API error: {response.status_code} - {response.text}")
            return None
        
        # Response is MP3 audio bytes
        audio_bytes = response.content
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        
        logger.info(f"Successfully generated TTS audio ({len(audio_base64)} bytes base64)")
        return audio_base64
        
    except Exception as e:
        logger.error(f"Error generating TTS: {e}")
        return None
