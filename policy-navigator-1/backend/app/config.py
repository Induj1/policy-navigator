from pydantic import BaseSettings

class Settings(BaseSettings):
    # Application settings
    app_name: str = "Policy Navigator"
    app_version: str = "0.1.0"
    
    # Database settings
    database_url: str
    
    # Other settings can be added here
    # For example, you might want to add settings for API keys, etc.

    class Config:
        env_file = ".env"  # Load environment variables from a .env file

settings = Settings()