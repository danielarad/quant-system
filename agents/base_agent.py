"""
agents/base_agent.py
--------------------
Abstract Base Agent.

Defines the interface that all specialist agents must implement.

Design rationale:
    - Using an ABC enforces a consistent contract across all agents.
    - The MetaAgent can call agent.analyze(data) on any agent without
      knowing which concrete class it is talking to.
    - Adding a new agent = create a new class, inherit BaseAgent,
      implement analyze(). Nothing else changes.

Future extension:
    - Add run_async() for concurrent agent execution.
    - Add validate(data) to enforce input schemas.
    - Add to_dict() to serialize agent output for API responses.
"""

from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """
    Abstract base class for all specialist agents.

    Every agent in the system must:
        1. Inherit from BaseAgent.
        2. Implement the analyze() method.
        3. Accept a data dict as input.
        4. Return a formatted string — never print directly.
    """

    @property
    def name(self) -> str:
        """
        Human-readable agent name.
        Defaults to the class name. Override in subclass if needed.
        """
        return self.__class__.__name__

    @abstractmethod
    def analyze(self, data: dict) -> str:
        """
        Run the agent's analysis on the provided market data.

        Args:
            data: A structured dict from data_loader.
                  Expected keys: asset, symbol, price (float), timestamp (str).

        Returns:
            A formatted multi-line string with the agent's findings.
            The output will be displayed directly in the CLI.
        """
        ...

    def __repr__(self) -> str:
        return f"<Agent: {self.name}>"
