"""Scanner initialization."""

from .library import Library
from .local_scanner import LocalScanner


def init_scanners(library: Library) -> None:
    """Initialize all built-in scanners.
    
    Args:
        library: Scanner library to add scanners to
    """
    # Add local scanner
    library.add_scanner(LocalScanner())
    
    # Note: Other scanners (Numverify, Google Search, OVH, Google CSE) 
    # would be added here. They require external API keys and suppliers,
    # so they're omitted from this basic conversion.
    
    # Load any registered plugins
    library.load_plugins()
