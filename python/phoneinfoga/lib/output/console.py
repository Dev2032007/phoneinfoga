"""Console output formatter."""

import logging
from typing import Dict, Any, TextIO, List
from dataclasses import fields, is_dataclass
from colorama import Fore, Style, init as colorama_init

from .output import Output

# Initialize colorama for cross-platform color support
colorama_init(autoreset=True)

logger = logging.getLogger(__name__)


class ConsoleOutput(Output):
    """Console output formatter with color support."""
    
    def __init__(self, writer: TextIO):
        """Initialize console output.
        
        Args:
            writer: Text stream to write output to
        """
        self.writer = writer
    
    def write(self, results: Dict[str, Any], errors: Dict[str, Exception]) -> None:
        """Write scan results and errors to console.
        
        Args:
            results: Dictionary of scanner results
            errors: Dictionary of scanner errors
        """
        succeeded = 0
        
        # Display results
        for name in sorted(results.keys()):
            result = results[name]
            if result is None:
                logger.debug(f"Scanner {name} returned result <nil>")
                continue
            
            self.writer.write(f"{Style.BRIGHT}Results for {name}{Style.RESET_ALL}\n")
            self._display_result(result, "")
            self.writer.write("\n")
            succeeded += 1
        
        # Display errors
        if errors:
            self.writer.write("The following scanners returned errors:\n")
            for name in sorted(errors.keys()):
                self.writer.write(f"{name}: {errors[name]}\n")
            self.writer.write("\n")
        
        # Summary
        self.writer.write(f"{succeeded} scanner(s) succeeded\n")
    
    def _display_result(self, value: Any, prefix: str) -> None:
        """Display a result value with proper formatting.
        
        Args:
            value: Value to display
            prefix: Indentation prefix for nested values
        """
        # Handle lists
        if isinstance(value, list):
            for i, item in enumerate(value):
                self._display_result(item, prefix)
                if i < len(value) - 1:
                    self.writer.write("\n")
            return
        
        # Handle dictionaries
        if isinstance(value, dict):
            for key, val in value.items():
                self._write_field(key, val, prefix)
            return
        
        # Handle dataclasses
        if is_dataclass(value):
            for field in fields(value):
                field_value = getattr(value, field.name)
                
                # Check for console tag in metadata
                console_tag = field.metadata.get("console")
                if console_tag == "-":
                    continue
                
                # Use field name as display name
                display_name = field.name.replace("_", " ").title()
                
                # Skip empty values if omitempty is specified
                if console_tag and "omitempty" in console_tag:
                    if field_value is None or field_value == "" or field_value == 0:
                        continue
                
                self._write_field(display_name, field_value, prefix)
            return
        
        # Handle objects with __dict__
        if hasattr(value, "__dict__"):
            for key, val in value.__dict__.items():
                if not key.startswith("_"):
                    display_name = key.replace("_", " ").title()
                    self._write_field(display_name, val, prefix)
            return
    
    def _write_field(self, name: str, value: Any, prefix: str) -> None:
        """Write a single field with appropriate formatting.
        
        Args:
            name: Field name
            value: Field value
            prefix: Indentation prefix
        """
        if isinstance(value, str):
            self.writer.write(f"{prefix}{name}: {Fore.YELLOW}{value}{Style.RESET_ALL}\n")
        elif isinstance(value, bool):
            self.writer.write(f"{prefix}{name}: {Fore.YELLOW}{value}{Style.RESET_ALL}\n")
        elif isinstance(value, int):
            self.writer.write(f"{prefix}{name}: {Fore.YELLOW}{value}{Style.RESET_ALL}\n")
        elif isinstance(value, (dict, list)) or is_dataclass(value) or hasattr(value, "__dict__"):
            self.writer.write(f"{Style.BRIGHT}{name}:{Style.RESET_ALL}\n")
            self._display_result(value, prefix + "\t")
        else:
            self.writer.write(f"{prefix}{name}: {Fore.YELLOW}{value}{Style.RESET_ALL}\n")
