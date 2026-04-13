"""
config/settings.py
------------------
Central configuration file.

All constants, API endpoints, and file paths live here.
No magic strings scattered across the codebase.
To extend: add new constants here; import them where needed.
"""

import os

# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------

# Binance public spot ticker — no API key required
BINANCE_TICKER_URL = "https://api.binance.com/api/v3/ticker/price"

# Default trading pair
DEFAULT_SYMBOL = "BTCUSDT"

# ---------------------------------------------------------------------------
# Storage
# ---------------------------------------------------------------------------

# Absolute path to storage.json, relative to this file's location
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORAGE_FILE = os.path.join(_BASE_DIR, "db", "storage.json")

# ---------------------------------------------------------------------------
# Request settings
# ---------------------------------------------------------------------------

REQUEST_TIMEOUT = 10  # seconds

# ---------------------------------------------------------------------------
# Price-level thresholds (used by agents for regime classification)
# Easy to update without touching agent logic.
# ---------------------------------------------------------------------------

PRICE_STRONG_BULL = 70_000
PRICE_MILD_BULL   = 50_000
PRICE_BEAR        = 30_000

PRICE_CYCLE_TOP   = 90_000
PRICE_BULL_MARKET = 50_000
PRICE_BEAR_MARKET = 25_000
