import os
from dotenv import load_dotenv

load_dotenv()

STEAM_API_KEY = os.getenv("STEAM_API_KEY")


def require_steam_api_key() -> str:
    if not STEAM_API_KEY:
        raise RuntimeError(
            "STEAM_API_KEY is not set. "
            "Create a .env file in the project root with STEAM_API_KEY=your_key_here."
        )
    return STEAM_API_KEY
