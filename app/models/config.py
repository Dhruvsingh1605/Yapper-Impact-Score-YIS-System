from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    # Embedding model name for sentence-transformers
    EMBED_MODEL_NAME: str = "all-MiniLM-L6-v2"

    # Weight multipliers for engagement components
    WEIGHTS: dict = {
        "retweet": 5,
        "reply": 3,
        "like": 1.5,
    }

    class Config:
        # You can load from a .env file or environment variables
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create a single, global settings instance
settings = Settings()

# Export constants for easy import
EMBED_MODEL_NAME = settings.EMBED_MODEL_NAME
WEIGHTS = settings.WEIGHTS
