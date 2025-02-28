from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    hotels_apikey: str
    openai_endpoint: str
    openai_apikey: str
    openai_version: str
    openai_model: str
    class Config:
        env_file = ".env"
        
settings = Settings()