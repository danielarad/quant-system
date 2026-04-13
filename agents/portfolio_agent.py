"""
agents/portfolio_agent.py
-------------------------
Portfolio Agent — Allocation and Sizing Layer.

Generates a BTC vs. cash allocation recommendation based on price regime.
In production this would run mean-variance optimization, Kelly Criterion,
or risk-parity weighting across multiple assets.
The return structure is extensible: add more asset slots easily.

Inherits: BaseAgent
Input:    data dict from data_loader
Output:   formatted string (returned, never printed)
"""

from agents.base_agent import BaseAgent
from utils.logger import log


# Allocation schedule: list of (min_price, btc_pct, cash_pct, rationale).
# Evaluated top-to-bottom; first match wins.
# Easily extended to add stablecoin buckets, bonds, equities, etc.
_ALLOCATION_SCHEDULE = [
    (90_000, 20,  80, "Near cycle top — heavy cash reserve, minimal BTC exposure."),
    (70_000, 35,  65, "Upper range — reduced BTC weight, protect gains."),
    (50_000, 50,  50, "Mid range — balanced equal-weight allocation."),
    (30_000, 65,  35, "Recovery zone — increased BTC weight for cycle upside."),
    (     0, 80,  20, "Deep value zone — maximum BTC accumulation allocation."),
]

# Risk-per-trade sizing: conservative when heavily long, slightly looser in bear zones
_RISK_PER_TRADE = {
    "high_btc":  1.0,   # btc_pct >= 60: size conservatively
    "low_btc":   2.0,   # btc_pct < 60:  slightly looser, smaller base
}


class PortfolioAgent(BaseAgent):
    """
    Recommends a portfolio allocation based on current BTC price regime.
    """

    def analyze(self, data: dict) -> str:
        """
        Generate a portfolio allocation recommendation.

        Args:
            data: Dict with keys: asset, price (float), timestamp.

        Returns:
            Multi-line allocation recommendation string.
        """
        price = data.get("price")
        if price is None:
            log("warning", self.name, "Received data with no price field.")
            return "  [Portfolio Agent] Insufficient data."

        btc_pct, cash_pct, rationale = self._get_allocation(price)
        risk_per_trade = (
            _RISK_PER_TRADE["high_btc"] if btc_pct >= 60
            else _RISK_PER_TRADE["low_btc"]
        )

        return (
            f"  BTC Price              : ${price:,.2f}\n"
            f"  Recommended BTC Weight : {btc_pct}%\n"
            f"  Recommended Cash Weight: {cash_pct}%\n"
            f"  Risk Per Trade         : {risk_per_trade}% of portfolio\n"
            f"  Rationale              : {rationale}\n"
            f"  Rebalance Trigger      : Reassess at +/-10% price move."
        )

    def _get_allocation(self, price: float) -> tuple[int, int, str]:
        """
        Walk the allocation schedule and return the matching entry.

        Args:
            price: Current BTC price.

        Returns:
            Tuple of (btc_pct, cash_pct, rationale).
        """
        for min_price, btc_pct, cash_pct, rationale in _ALLOCATION_SCHEDULE:
            if price >= min_price:
                return btc_pct, cash_pct, rationale

        # Fallback: should never reach here if schedule covers 0+
        return 50, 50, "Default balanced allocation."
