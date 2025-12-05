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
