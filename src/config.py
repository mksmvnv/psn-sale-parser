from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DOMAIN_NAME: str
    CATEGORY_URL: str
    USER_AGENT: str
    PROXIES: str

    class Config:
        env_file = ".env"


settings = Settings()
