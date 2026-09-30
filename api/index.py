import os
import sys
from pathlib import Path

# Set up module resolution paths
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from server import app

# Vercel ASGI Handler
handler = app
