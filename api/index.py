import sys
import os
from pathlib import Path

# Add project root to sys.path so app/ package is importable
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Load .env if present (local dev); Vercel injects env vars automatically
try:
    from dotenv import load_dotenv
    load_dotenv(ROOT_DIR / ".env")
except ImportError:
    pass

from app.main import app  # noqa: E402 — must come after sys.path patch
