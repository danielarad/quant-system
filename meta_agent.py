"""
meta_agent.py
-------------
The Orchestrator (Meta-Agent).

Responsibilities:
    1. Parse the user query for intent using keyword detection.
    2. Fetch live market data via the data layer.
    3. Persist the data snapshot via the storage layer.
    4. Route the query to the appropriate specialist agent.
    5. Return the structured, formatted response.

Design principle:
    The meta-agent knows ABOUT agents but does not contain agent logic.
    Each agent is independent — adding a new agent = add it to the
    routing table. No other code changes required.

Future extension:
    Replace keyword routing with an LLM intent classifier.
    Add concurrent agent execution (asyncio.gather).
    Add response aggregation and scoring.
"""

from agents.quant_agent import QuantAgent
from agents.macro_agent import MacroAgent
from agents.portfolio_agent import PortfolioAgent
from data.data_loader import get_btc_price
from db.database import save_data
from utils.logger import log, log_separator


# ---------------------------------------------------------------------------
# Intent Routing Table
# Maps keyword sets to agent names. Add entries here to extend routing.
# ---------------------------------------------------------------------------
_ROUTING_TABLE = {
    "quant":     ["strategy", "trade", "signal", "momentum", "trend", "technical"],
    "macro":     ["market", "macro", "condition", "economy", "regime", "cycle"],
    "portfolio": ["portfolio", "allocation", "weight", "position", "sizing", "exposure"],
}


class MetaAgent:
    """
    Central orchestrator.
    Detects intent → fetches data → routes to specialist agent → returns response.
    """

    def __init__(self):
        # Instantiate agents once — reused across queries.
        self._agents = {
            "quant":     QuantAgent(),
            "macro":     MacroAgent(),
            "portfolio": PortfolioAgent(),
        }
        log("info", "MetaAgent", "Initialized with agents: " + ", ".join(self._agents.keys()))

    def route(self, query: str) -> str:
        """
        Main entry point: parse query, fetch data, delegate to agent.

        Args:
            query: Raw user input string.

        Returns:
            Formatted response string from the relevant agent(s).
            Returns an error message string on data fetch failure.
        """
        # 1. Fetch live data
        log("info", "MetaAgent", "Fetching live BTC data...")
        market_data = get_btc_price()

        if market_data is None:
            return ("[Error] Could not fetch BTC price data.\n"
                    "Check your network connection and try again.")

        # 2. Persist snapshot to storage
        save_data(market_data)

        # 3. Detect intent
        intent = self._detect_intent(query)
        log("info", "MetaAgent", f"Detected intent: {intent}")

        # 4. Route to agent(s)
        if intent and intent in self._agents:
            log("info", "MetaAgent", f"Routing to {intent} agent.")
            return self._agents[intent].analyze(market_data)
        else:
            # Default: run full analysis with all agents
            log("info", "MetaAgent", "No specific intent detected — running full analysis.")
            return self._run_full_analysis(market_data)

    def _detect_intent(self, query: str) -> str | None:
        """
        Scan the query for known keywords and return the matching intent key.

        Args:
            query: Raw user input.

        Returns:
            An intent string ("quant", "macro", "portfolio"), or None.
        """
        q = query.lower()
        for intent, keywords in _ROUTING_TABLE.items():
            if any(kw in q for kw in keywords):
                return intent
        return None

    def _run_full_analysis(self, market_data: dict) -> str:
        """
        Run all agents and return a combined report.

        Args:
            market_data: Structured dict from data_loader.

        Returns:
            Multi-section full analysis string.
        """
        sections = []
        for label, agent in self._agents.items():
            sections.append(f"[ {label.upper()} AGENT ]")
            sections.append(agent.analyze(market_data))
            sections.append("")

        return "\n".join(sections)
