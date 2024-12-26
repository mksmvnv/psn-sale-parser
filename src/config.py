from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DOMAIN_NAME: str
    CATEGORY_PATH: str
    USER_AGENT: str
    PROXY: str
    JSON_PATH: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
