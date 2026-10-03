import os

from dotenv import load_dotenv
from openai import AsyncOpenAI

from agents import (
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
)


load_dotenv()

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434/v1",
)

OLLAMA_API_KEY = os.getenv(
    "OLLAMA_API_KEY",
    "ollama",
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen3:4b",
)


set_tracing_disabled(True)


client = AsyncOpenAI(
    base_url=OLLAMA_BASE_URL,
    api_key=OLLAMA_API_KEY,
)


model = OpenAIChatCompletionsModel(
    model=OLLAMA_MODEL,
    openai_client=client,
)