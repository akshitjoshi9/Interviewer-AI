from pydantic_settings import BaseSettings
from langchain_openai import ChatOpenAI
from openai import OpenAI


class Settings(BaseSettings):

    DATABASE_URL_ENGINE: str
    OPENAI_API_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
    api_key=settings.OPENAI_API_KEY,
)
