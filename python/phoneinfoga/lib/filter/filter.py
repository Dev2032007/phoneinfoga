"""Filter engine for scanner selection."""

from abc import ABC, abstractmethod
from typing import List


class Filter(ABC):
    """Abstract base class for filters."""
    
    @abstractmethod
    def match(self, value: str) -> bool:
        """Check if a value matches the filter.
        
        Args:
            value: Value to check against the filter
            
        Returns:
            bool: True if the value matches, False otherwise
        """
        pass


class Engine(Filter):
    """Filter engine for matching scanner names against rules.
    
    The engine maintains a list of rules (scanner names) and can check
    if a given scanner name matches any of the rules.
    """
    
    def __init__(self) -> None:
        """Initialize an empty filter engine."""
        self.rules: List[str] = []
    
    def add_rule(self, *rules: str) -> None:
        """Add one or more rules to the filter.
        
        Args:
            *rules: Scanner names to add as filter rules
        """
        self.rules.extend(rules)
    
    def match(self, value: str) -> bool:
        """Check if a value matches any of the filter rules.
        
        Args:
            value: Scanner name to check
            
        Returns:
            bool: True if the value matches any rule, False otherwise
        """
        return value in self.rules
