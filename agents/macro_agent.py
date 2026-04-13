"""
agents/macro_agent.py
---------------------
Macro Agent — Market Condition / Cycle Assessment Layer.

Classifies the macro environment based on BTC price level.
In production this would consume Fed rates, CPI, BTC dominance,
on-chain metrics (SOPR, NVT, exchange flows), and risk sentiment.
The architecture is identical — replace the logic, keep the interface.

Inherits: BaseAgent
Input:    data dict from data_loader
Output:   formatted string (returned, never printed)
"""

from agents.base_agent import BaseAgent
from config.settings import PRICE_CYCLE_TOP, PRICE_BULL_MARKET, PRICE_BEAR_MARKET
from utils.logger import log


# Macro regime definitions.
# Each entry: (min_price, condition_label, environment_desc, risk_level, analyst_note)
_MACRO_REGIMES = [
    (
        PRICE_CYCLE_TOP,
        "LATE BULL / DISTRIBUTION",
        "Historically elevated valuations. Mean reversion risk is high.",
        "HIGH",
        "Risk-off posture warranted. Watch for liquidity tightening signals."
    ),
    (
        PRICE_BULL_MARKET,
        "MID BULL MARKET",
        "Price in healthy bull territory. Macro tailwinds likely present.",
        "MEDIUM",
        "Monitor Fed policy and USD strength for trend continuation."
    ),
    (
        PRICE_BEAR_MARKET,
        "ACCUMULATION / EARLY RECOVERY",
        "Price recovering from lows. Macro uncertainty likely elevated.",
        "MEDIUM-HIGH",
        "Watch for improving on-chain fundamentals and volume confirmation."
    ),
    (
        0,
        "DEEP BEAR MARKET",
        "Price at cyclically depressed levels. Macro headwinds dominant.",
        "VERY HIGH",
        "Capital preservation is priority. Await macro regime shift signals."
    ),
]


class MacroAgent(BaseAgent):
    """
    Assesses the macro-level market environment based on BTC price level.
    """

    def analyze(self, data: dict) -> str:
        """
        Classify macro regime and return a structured assessment.

        Args:
            data: Dict with keys: asset, price (float), timestamp.

        Returns:
            Multi-line macro condition summary string.
        """
        price = data.get("price")
        if price is None:
            log("warning", self.name, "Received data with no price field.")
            return "  [Macro Agent] Insufficient data."

        ts = data.get("timestamp", "N/A")
        condition, environment, risk_level, note = self._classify_macro(price)

        return (
            f"  Timestamp         : {ts}\n"
            f"  BTC Price         : ${price:,.2f}\n"
            f"  Market Condition  : {condition}\n"
            f"  Environment       : {environment}\n"
            f"  Macro Risk Level  : {risk_level}\n"
            f"  Analyst Note      : {note}"
        )

    def _classify_macro(self, price: float) -> tuple:
        """
        Walk the regime table and return the matching macro classification.

        Args:
            price: Current BTC price.

        Returns:
            Tuple of (condition, environment, risk_level, note).
        """
        for min_price, condition, environment, risk_level, note in _MACRO_REGIMES:
            if price >= min_price:
                return condition, environment, risk_level, note

        # Fallback (should never reach here if table is correct)
        return "UNKNOWN", "Unable to classify.", "UNKNOWN", "Review price thresholds."
