"""
main.py
-------
CLI Entry Point for the Quant System.

This file is the only user-facing interface. It:
    - Accepts user queries from stdin.
    - Passes them to the MetaAgent.
    - Displays the formatted response.

Design: this file contains ZERO business logic.
To add an API layer later: replace this file with FastAPI.
The MetaAgent.route() call stays identical.
"""

import sys
from meta_agent import MetaAgent
from utils.logger import log, log_separator


BANNER = [
    "=======================================================",
    "   QUANT SYSTEM -- Multi-Agent Trading Intelligence   ",
    "   v1.0 MVP  |  Live BTC Data  |  3-Agent System     ",
    "=======================================================",
    "",
    "  Available query types:",
    "    Strategy signal  -->  give me a trade strategy",
    "    Macro conditions -->  what is the market condition",
    "    Portfolio        -->  suggest a portfolio allocation",
    "    Full analysis    -->  any other input",
    "",
    "  Type exit or quit to stop.",
]


def main() -> None:
    """
    Run the interactive CLI loop.
    Gracefully exits on KeyboardInterrupt or EOF.
    """
    print("\n".join(BANNER))
    log("info", "System", "MetaAgent initializing...")

    try:
        agent = MetaAgent()
    except Exception as e:
        log("error", "System", f"Failed to initialize MetaAgent: {e}")
        sys.exit(1)

    log("info", "System", "Ready. Awaiting queries.")
    log_separator()

    while True:
        try:
            user_input = input("\n>>> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n")
            log("info", "System", "Shutdown requested. Goodbye.")
            break

        if not user_input:
            print("  [Hint] Please enter a query or type exit to quit.")
            continue

        if user_input.lower() in ("exit", "quit", "q"):
            log("info", "System", "Goodbye.")
            break

        log_separator()

        try:
            response = agent.route(user_input)
            print(f"\n{response}\n")
        except Exception as e:
            log("error", "System", f"Unhandled error during routing: {e}")
            print(f"  [Error] Something went wrong: {e}")

        log_separator()


if __name__ == "__main__":
    main()
