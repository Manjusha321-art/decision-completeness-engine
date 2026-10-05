"""
Base class for source connectors in the Decision Completeness Engine.
Connectors search external systems (Drive, Email, ERP, Web Registry)
for missing evidence to achieve autonomous self-healing.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseConnector(ABC):
    """Abstract connector interface for evidence discovery."""

    def __init__(self, name: str, source_type: str):
        self.name = name
        self.source_type = source_type

    @abstractmethod
    def search(self, queries: List[str], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Search the connected source for documents or records matching the queries.
        Returns a list of candidate evidence payloads with:
          - source_location: str
          - title: str
          - content_snippet: str
          - confidence: float
          - metadata: dict
        """
        pass
