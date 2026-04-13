# quant-system

> **Modular multi-agent quantitative trading system MVP**
> Meta-Agent orchestrator | Specialized agents | Live BTC data | JSON storage
> Designed as a scalable hedge-fund research skeleton.

---

## System Overview

`quant-system` is a clean, production-structured Python project that simulates
the architecture of a hedge-fund research platform. It is not a single script.
It is a modular, layered system where every component has a single, well-defined
responsibility.

The system fetches **live BTC/USDT price data** from the Binance public API,
stores it locally, and routes user queries to the appropriate specialist agent.

---

## Architecture

```
quant-system/
|
+-- main.py            # CLI entry point (no business logic)
+-- meta_agent.py      # Orchestrator: detects intent, routes to agents
|
+-- agents/
|   +-- base_agent.py       # Abstract base class (agent contract)
|   +-- quant_agent.py      # Technical/strategy signals
|   +-- macro_agent.py      # Market cycle/condition assessment
|   +-- portfolio_agent.py  # Allocation and sizing recommendations
|
+-- data/
|   +-- data_loader.py      # Fetches live BTC price from Binance
|
+-- db/
|   +-- database.py         # JSON storage abstraction layer
|   +-- storage.json        # Auto-created on first run
|
+-- config/
|   +-- settings.py         # All constants and configuration
|
+-- utils/
|   +-- logger.py           # Reusable structured logging utility
|
+-- requirements.txt
+-- .gitignore
```

---

## Layer Responsibilities

| Layer | File(s) | Responsibility |
|-------|---------|----------------|
| Entry | `main.py` | User-facing CLI. No logic. |
| Orchestration | `meta_agent.py` | Intent detection, routing, data coordination |
| Agent | `agents/*.py` | Specialist analysis and signal generation |
| Data | `data/data_loader.py` | External API calls (Binance) |
| Storage | `db/database.py` | All file I/O. Single source of truth for persistence |
| Config | `config/settings.py` | All constants. No magic strings in code |
| Utils | `utils/logger.py` | Logging utility. Replaces raw print() |

**No layer reaches into another layer's responsibilities.**

---

## How Agents Work

Every agent inherits from `BaseAgent` and implements a single method:

```python
def analyze(self, data: dict) -> str:
    ...
```

The `MetaAgent` (orchestrator) uses **keyword-based intent detection** to
decide which agent to call:

| User query contains... | Routes to |
|------------------------|-----------|
| "strategy", "trade", "signal" | `QuantAgent` |
| "market", "macro", "condition" | `MacroAgent` |
| "portfolio", "allocation", "weight" | `PortfolioAgent` |
| anything else | All agents (full report) |

Agents **receive** data via parameters. They never fetch data themselves.
This enforces clean separation of concerns.

---

## How to Run Locally (macOS)

### 1. Clone the repository

```bash
git clone https://github.com/danielarad/quant-system.git
cd quant-system
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the system

```bash
python main.py
```

### 5. Example queries

```
>>> give me a trade strategy
>>> what is the market condition?
>>> suggest a portfolio allocation
>>> hello
```

---

## How to Extend the System

### Add a new agent
1. Create `agents/my_agent.py`
2. Inherit from `BaseAgent`, implement `analyze(self, data)`
3. Add it to `MetaAgent._agents` dict
4. Add routing keywords to `_ROUTING_TABLE` in `meta_agent.py`

### Add a new data source
1. Add a new fetch function in `data/data_loader.py`
2. Call it from `MetaAgent.route()` alongside `get_btc_price()`
3. Pass the new data into the relevant agent's `analyze()` call

### Change price thresholds
Edit `config/settings.py`. No agent files need to change.

---

## Future Roadmap

| Milestone | Description |
|-----------|-------------|
| **v1.1** | Add `ETHAgent` and multi-asset support via `data_loader.get_price(symbol)` |
| **v1.2** | Replace JSON storage with PostgreSQL (`db/database.py` interface unchanged) |
| **v1.3** | Add FastAPI layer — expose `/query` endpoint, `main.py` becomes optional |
| **v2.0** | Integrate LLM (Claude/GPT) as the intent router and response narrator |
| **v2.1** | Add async agent execution (`asyncio.gather`) for parallel analysis |
| **v2.2** | Add backtesting module — agents consume OHLCV history, not just spot price |
| **v3.0** | Multi-asset risk-parity portfolio optimizer with Kelly sizing |

---

## Requirements

- Python 3.10+
- `requests>=2.31.0` (only external dependency)
- macOS, Linux, or Windows
- Internet connection (for live BTC price fetch)

---

## License

MIT — free to use, extend, and build upon.
