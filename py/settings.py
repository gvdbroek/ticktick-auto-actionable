from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    ticktick_api_key: str = Field()
