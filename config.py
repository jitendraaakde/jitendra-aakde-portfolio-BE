import os

class Config:
    """
    Configuration class for the application.
    """

    def get_config_value(key, default=None):
        """Helper to fetch config values from secrets or environment."""
        return os.environ.get(key, default)
    
    # Unreal Speech TTS Configuration
    UNREAL_SPEECH_API_KEY = get_config_value("UNREAL_SPEECH_API_KEY", None)
    UNREAL_SPEECH_VOICE = get_config_value("UNREAL_SPEECH_VOICE", "Will")  # Will = Mature Male voice
    
    # Groq Configuration (Primary API, replacing Gemini)
    GROQ_API_KEY = get_config_value("GROQ_API_KEY", None)
    GROQ_MODEL = get_config_value("GROQ_MODEL", "llama-3.3-70b-versatile")
    
    # OpenRouter Configuration (Fallback for Groq)
    OPENROUTER_API_KEY = get_config_value("OPENROUTER_API_KEY", None)
    OPENROUTER_MODEL = get_config_value("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct:free")
