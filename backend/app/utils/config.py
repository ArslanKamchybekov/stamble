import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, Any
import logging

from .exceptions import ConfigurationError

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

class Config:
    """
    Configuration manager for the application.
    Handles environment variables and default settings.
    """
    
    # OpenAI API settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Application settings
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    ENV = os.getenv("ENV", "development")
    PORT = int(os.getenv("PORT", "8000"))
    
    # CORS settings
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    
    # Rate limiting
    RATE_LIMIT = int(os.getenv("RATE_LIMIT", "100"))  # Requests per hour
    
    @staticmethod
    def validate() -> None:
        """
        Validate that all required configuration is present
        """
        if not Config.OPENAI_API_KEY:
            raise ConfigurationError("OPENAI_API_KEY environment variable is required")
            
    @staticmethod
    def as_dict() -> Dict[str, Any]:
        """
        Return configuration as a dictionary (excluding sensitive values)
        """
        return {
            "debug": Config.DEBUG,
            "env": Config.ENV,
            "port": Config.PORT,
            "cors_origins": Config.CORS_ORIGINS,
            "rate_limit": Config.RATE_LIMIT,
        }
        
    @staticmethod
    def setup_logging() -> None:
        """
        Configure application logging
        """
        log_level = logging.DEBUG if Config.DEBUG else logging.INFO
        
        # Configure the root logger
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler()]
        )
        
        # Set specific loggers to different levels if needed
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("uvicorn").setLevel(logging.INFO)
        
        logger.debug("Logging configured with level: %s", log_level) 