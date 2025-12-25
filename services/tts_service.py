import base64
import re
import requests
from config import Config
from utils.logger import logger


def humanize_text(text: str) -> str:
    """
    Preprocess text to add natural pauses and improve speech flow.
    """
    # Add slight pauses after certain punctuation for natural rhythm
    text = re.sub(r'([.!?])\s+', r'\1 ', text)
    
    # Add commas before conjunctions for natural pauses if missing
    text = re.sub(r'\s+(and|but|or|so)\s+', r', \1 ', text, flags=re.IGNORECASE)
    
    # Clean up any double spaces or extra commas
    text = re.sub(r',\s*,', ',', text)
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


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
        
        # Preprocess text for more natural speech
        text = humanize_text(text)
        
        # Truncate to 1000 chars for stream endpoint
        if len(text) > 1000:
            text = text[:1000]
            logger.info(f"Truncated text to 1000 chars for Unreal Speech stream")
        
        voice = voice_id or Config.UNREAL_SPEECH_VOICE
        logger.info(f"Generating TTS with Unreal Speech voice: {voice}")
        
        # Use the /stream endpoint for fastest response
        # Speed: -0.05 for slightly slower, natural pace
        # Pitch: 1.0 for natural voice pitch
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
                "Speed": 0.1,
                "Pitch": 1.0
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
