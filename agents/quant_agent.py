"""
agents/quant_agent.py
---------------------
Quant Agent — Technical / Strategy Analysis Layer.

Analyzes BTC price structure and historical momentum.
Generates a directional bias signal with supporting rationale.

In a production system this would consume OHLCV data and run
indicators (RSI, MACD, ATR, Bollinger). The architecture is
identical — swap the logic here without touching the orchestrator.

Inherits: BaseAgent
Input:    data dict from data_loader
Output:   formatted string (returned, never printed)
"""

from agents.base_agent import BaseAgent
from config.settings import PRICE_STRONG_BULL, PRICE_MILD_BULL, PRICE_BEAR
from db.database import load_data
from utils.logger import log


class QuantAgent(BaseAgent):
    """
    Produces a short-term directional strategy signal based on:
        1. Price-level regime classification.
        2. Momentum: compares current price to last stored snapshot.
    """

    def analyze(self, data: dict) -> str:
        """
        Analyze current BTC data and return a strategy signal.

        Args:
            data: Dict with keys: asset, price (float), timestamp.

        Returns:
            Multi-line strategy insight string.
        """
        price = data.get("price")
        if price is None:
            log("warning", self.name, "Received data with no price field.")
            return "  [Quant Agent] Insufficient data to generate signal."

        momentum_note = self._compute_momentum(price)
        regime, bias, action = self._classify_regime(price)

        return (
            f"  BTC Price         : ${price:,.2f}\n"
            f"  Price Regime      : {regime}\n"
            f"  Directional Bias  : {bias}\n"
            f"  Suggested Action  : {action}\n"
            f"{momentum_note}"
        )

    def _classify_regime(self, price: float) -> tuple[str, str, str]:
        """
        Classify price into a structural regime.
        Thresholds are sourced from config/settings.py — easily adjustable.

        Returns:
            Tuple of (regime_label, bias_description, action_suggestion).
        """
        if price > PRICE_STRONG_BULL:
            return (
                "STRONG BULL ZONE",
                "Long bias — price in upper structural range.",
                "Consider momentum entries on pullbacks; keep stops tight."
            )
        elif price > PRICE_MILD_BULL:
            return (
                "MILD BULL ZONE",
                "Cautiously long — mid-range price structure.",
                "Wait for breakout confirmation before sizing up."
            )
        elif price > PRICE_BEAR:
            return (
                "NEUTRAL / RECOVERY ZONE",
                "No strong directional edge — range-bound likely.",
                "Reduce size; await trend confirmation signal."
            )
        else:
            return (
                "BEAR ZONE",
                "Short bias — price in lower structural range.",
                "Protect capital. Watch for capitulation / reversal signals."
            )

    def _compute_momentum(self, current_price: float) -> str:
        """
        Compare current price to the most recent stored snapshot.
        Returns a momentum label with percentage change.

        Returns:
            Formatted momentum string, or empty string if no history.
        """
        history = load_data()

        if len(history) < 2:
            return "  Momentum          : Insufficient history for comparison."

        prev_price = history[-1].get("price")
        if not prev_price or prev_price == 0:
            return "  Momentum          : Previous price unavailable."

        change_pct = ((current_price - prev_price) / prev_price) * 100

        if change_pct > 0.5:
            label = "BULLISH"
        elif change_pct < -0.5:
            label = "BEARISH"
        else:
            label = "NEUTRAL"

        sign = "+" if change_pct >= 0 else ""
        return f"  Momentum          : {label} ({sign}{change_pct:.2f}% vs last snapshot)"
