from pydantic import BaseSettings


class Settings(BaseSettings):
    CHANNEL_ACCESS_TOKEN: str


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
