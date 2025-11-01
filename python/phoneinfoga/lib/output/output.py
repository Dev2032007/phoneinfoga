"""Output interface and factory."""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any, TextIO
import sys


class Output(ABC):
    """Abstract base class for output formatters."""
    
    @abstractmethod
    def write(self, results: Dict[str, Any], errors: Dict[str, Exception]) -> None:
        """Write scan results and errors.
        
        Args:
            results: Dictionary of scanner results
            errors: Dictionary of scanner errors
        """
        pass


class OutputType(Enum):
    """Enumeration of available output types."""
    CONSOLE = "console"


def get_output(output_type: OutputType, writer: TextIO = None) -> Output:
    """Get an output formatter instance.
    
    Args:
        output_type: Type of output formatter to create
        writer: Text stream to write to (defaults to sys.stdout)
        
    Returns:
        Output: Output formatter instance
        
    Raises:
        ValueError: If output_type is not supported
    """
    from .console import ConsoleOutput
    
    if writer is None:
        writer = sys.stdout
    
    if output_type == OutputType.CONSOLE:
        return ConsoleOutput(writer)
    
    raise ValueError(f"Unsupported output type: {output_type}")
