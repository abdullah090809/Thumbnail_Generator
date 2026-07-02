from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Pollinations.ai
    POLLINATIONS_BASE_URL: str = "https://image.pollinations.ai/prompt"

    class Config:
        env_file = ".env"


settings = Settings()