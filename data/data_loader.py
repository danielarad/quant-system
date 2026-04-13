"""
data/data_loader.py
-------------------
Data Ingestion Layer.

All network I/O is isolated here — agents never call APIs directly.
Functions return structured dicts so callers receive typed, predictable data.
To add a new asset, add a new fetch function here.

Current sources:
    - Binance public REST API (no key required)
"""

import requests
from datetime import datetime, timezone

from config.settings import BINANCE_TICKER_URL, DEFAULT_SYMBOL, REQUEST_TIMEOUT
from utils.logger import log


def get_btc_price() -> dict | None:
    """
    Fetch the current BTC/USDT spot price from Binance public ticker API.

    Returns:
        dict with keys: asset, symbol, price (float), timestamp (ISO 8601)
        Returns None on any error — callers must handle None.
    """
    return get_price(DEFAULT_SYMBOL)


def get_price(symbol: str) -> dict | None:
    """
    Generic price fetcher for any Binance spot pair.

    Extension point: swap symbol to fetch ETH, SOL, or any Binance pair.
    Return structure is consistent across all assets.

    Args:
        symbol: Binance trading pair e.g. BTCUSDT, ETHUSDT, SOLUSDT.

    Returns:
        Structured price dict, or None on failure.
    """
    try:
        response = requests.get(
            BINANCE_TICKER_URL,
            params={"symbol": symbol.upper()},
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()

        raw = response.json()
        price = float(raw["price"])
        base = symbol.upper().replace("USDT", "")

        log("info", "DataLoader", f"Fetched {symbol}: ${price:,.2f}")

        return {
            "asset":     f"{base}/USDT",
            "symbol":    symbol.upper(),
            "price":     price,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except requests.exceptions.ConnectionError:
        log("error", "DataLoader", "Connection error — check network.")
    except requests.exceptions.Timeout:
        log("error", "DataLoader", f"Request timed out after {REQUEST_TIMEOUT}s.")
    except requests.exceptions.HTTPError as e:
        log("error", "DataLoader", f"HTTP error: {e}")
    except (KeyError, ValueError) as e:
        log("error", "DataLoader", f"Unexpected API response: {e}")
    except Exception as e:
        log("error", "DataLoader", f"Unhandled error: {e}")

    return None
