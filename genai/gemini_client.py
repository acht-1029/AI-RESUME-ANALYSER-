import os
import logging
from google import genai
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

class GeminiClient:
    """
    A robust wrapper around the Google Gemini API.
    Handles authentication and provides graceful fallbacks if the API key is missing.
    """
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.is_configured = False
        self.client = None
        
        # Check if the key is missing or still set to the default placeholder
        if not self.api_key or self.api_key == "YOUR_API_KEY_HERE":
            logger.warning("GEMINI_API_KEY not found in .env. GenAI features will be disabled.")
        else:
            try:
                self.client = genai.Client(api_key=self.api_key)
                # Using gemini-2.5-flash as the standard fast/cheap model
                self.model_name = 'gemini-2.5-flash'
                self.is_configured = True
            except Exception as e:
                logger.error(f"Failed to configure Gemini API: {e}")

    def generate_content(self, prompt: str) -> str:
        """
        Send a prompt to Gemini and return the text response.
        Returns an empty string if the API is not configured or if the request fails.
        """
        if not self.is_configured or not self.client:
            return ""
            
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini generation failed: {e}")
            return ""
