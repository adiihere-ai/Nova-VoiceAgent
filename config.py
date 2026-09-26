import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

@dataclass(frozen=True)
class Config:
    # LiveKit
    LIVEKIT_URL: str = os.getenv("LIVEKIT_URL", "")
    LIVEKIT_API_KEY: str = os.getenv("LIVEKIT_API_KEY", "")
    LIVEKIT_API_SECRET: str = os.getenv("LIVEKIT_API_SECRET", "")

    # Ollama / LLM
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://localhost:11434/v1")
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "llama3")

    # OpenAI Fallback
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    def validate(self):
        missing = []
        if not self.LIVEKIT_URL: missing.append("LIVEKIT_URL")
        if not self.LIVEKIT_API_KEY: missing.append("LIVEKIT_API_KEY")
        if not self.LIVEKIT_API_SECRET: missing.append("LIVEKIT_API_SECRET")

        if missing:
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

config = Config()
config.validate()
