import os

class Config:
    """
    Configuration class for the application.
    """

    def get_config_value(key, default=None):
        """Helper to fetch config values from secrets or environment."""
        return os.environ.get(key, default)
    
    # Multiple Gemini API Keys for fallback (from different Google AI Studio accounts)
    GEMINI_API_KEY_1 = get_config_value("GEMINI_API_KEY_1", None)
    GEMINI_API_KEY_2 = get_config_value("GEMINI_API_KEY_2", None)
    GEMINI_API_KEY_3 = get_config_value("GEMINI_API_KEY_3", None)
    GEMINI_MODEL_NAME = get_config_value("GEMINI_MODEL_NAME", "gemini-2.5-flash-lite")
    
    @staticmethod
    def get_gemini_api_keys():
        """Get list of configured Gemini API keys (non-empty only)."""
        keys = []
        for key in [Config.GEMINI_API_KEY_1, Config.GEMINI_API_KEY_2, Config.GEMINI_API_KEY_3]:
            if key:
                keys.append(key)
        return keys
    
    # Unreal Speech TTS Configuration
    UNREAL_SPEECH_API_KEY = get_config_value("UNREAL_SPEECH_API_KEY", None)
    UNREAL_SPEECH_VOICE = get_config_value("UNREAL_SPEECH_VOICE", "Will")  # Will = Mature Male voice
    
    # OpenRouter Configuration (Fallback for Gemini)
    OPENROUTER_API_KEY = get_config_value("OPENROUTER_API_KEY", None)
    OPENROUTER_MODEL = get_config_value("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct:free")
