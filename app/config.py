from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    salamandra_url: str = "http://localhost:8000/v1"
    salamandra_api_key: str = ""
    salamandra_model: str = "BSC-LT/salamandraTA-7b-instruct"
    port: int = 80
    host: str = "0.0.0.0"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
