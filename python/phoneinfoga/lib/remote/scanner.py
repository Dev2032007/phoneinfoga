"""Scanner interface and base classes."""

import os
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass

from phoneinfoga.lib.number import Number


class ScannerOptions(dict):
    """Options for scanner execution.
    
    This is a dictionary that can also retrieve values from environment variables.
    """
    
    def get_string_env(self, key: str, default: str = "") -> str:
        """Get a string value from options or environment.
        
        Args:
            key: Key to look up
            default: Default value if key not found
            
        Returns:
            str: Value from options, environment, or default
        """
        if key in self:
            value = self[key]
            if isinstance(value, str):
                return value
        return os.getenv(key, default)


class Scanner(ABC):
    """Abstract base class for all scanners."""
    
    @abstractmethod
    def name(self) -> str:
        """Get the scanner name.
        
        Returns:
            str: Scanner name
        """
        pass
    
    @abstractmethod
    def description(self) -> str:
        """Get the scanner description.
        
        Returns:
            str: Scanner description
        """
        pass
    
    @abstractmethod
    def dry_run(self, number: Number, options: ScannerOptions) -> Optional[Exception]:
        """Check if the scanner should run for this number.
        
        Args:
            number: Phone number to scan
            options: Scanner options
            
        Returns:
            Optional[Exception]: Exception if scanner should not run, None otherwise
        """
        pass
    
    @abstractmethod
    def run(self, number: Number, options: ScannerOptions) -> Any:
        """Run the scanner on a phone number.
        
        Args:
            number: Phone number to scan
            options: Scanner options
            
        Returns:
            Any: Scanner results
            
        Raises:
            Exception: If scanner execution fails
        """
        pass


def open_plugin(path: str) -> None:
    """Open and load a scanner plugin.
    
    Args:
        path: Path to the plugin file
        
    Raises:
        FileNotFoundError: If the plugin file doesn't exist
        ImportError: If the plugin cannot be loaded
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Given path {path} does not exist")
    
    # In Python, we would use importlib to dynamically load modules
    # This is a simplified version - full implementation would use importlib
    raise NotImplementedError("Plugin loading not yet implemented")
