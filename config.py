import os

class Config:
    """
    Configuration class for the application.
    """

    def get_config_value(key, default=None):
        """Helper to fetch config values from secrets or environment."""
        return os.environ.get(key, default)
    
    GEMINI_API_KEY = get_config_value("GEMINI_API_KEY", None)
    GEMINI_MODEL_NAME = get_config_value("GEMINI_MODEL_NAME", "gemini-2.5-flash-lite")
    
    # Unreal Speech TTS Configuration
    UNREAL_SPEECH_API_KEY = get_config_value("UNREAL_SPEECH_API_KEY", None)
    UNREAL_SPEECH_VOICE = get_config_value("UNREAL_SPEECH_VOICE", "Will")  # Will = Mature Male voice
    
    # OpenRouter Configuration (Fallback for Gemini)
    OPENROUTER_API_KEY = get_config_value("OPENROUTER_API_KEY", None)
    OPENROUTER_MODEL = get_config_value("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct:free")
