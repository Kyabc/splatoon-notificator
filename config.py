from pydantic import BaseSettings


class Settings(BaseSettings):
    CHANNEL_ACCESS_TOKEN: str
    USER_AGENT: str
    MAX_API_REQUESTS: int


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
