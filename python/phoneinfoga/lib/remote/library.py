"""Scanner library for managing and executing scanners."""

import logging
from typing import Dict, List, Any, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

from phoneinfoga.lib.number import Number
from phoneinfoga.lib.filter import Filter
from .scanner import Scanner, ScannerOptions

logger = logging.getLogger(__name__)


# Global plugin registry
_plugins: List[Scanner] = []
_plugins_lock = Lock()


def register_plugin(scanner: Scanner) -> None:
    """Register a scanner plugin.
    
    Args:
        scanner: Scanner instance to register
    """
    with _plugins_lock:
        _plugins.append(scanner)


class Library:
    """Library for managing and executing scanners."""
    
    def __init__(self, filter_engine: Filter):
        """Initialize the scanner library.
        
        Args:
            filter_engine: Filter engine for scanner selection
        """
        self._lock = Lock()
        self._scanners: List[Scanner] = []
        self._results: Dict[str, Any] = {}
        self._errors: Dict[str, Exception] = {}
        self._filter = filter_engine
    
    def load_plugins(self) -> None:
        """Load all registered plugins."""
        with _plugins_lock:
            for scanner in _plugins:
                self.add_scanner(scanner)
    
    def add_scanner(self, scanner: Scanner) -> None:
        """Add a scanner to the library.
        
        Args:
            scanner: Scanner instance to add
        """
        if self._filter.match(scanner.name()):
            logger.debug(f"Scanner {scanner.name()} was ignored by filter")
            return
        self._scanners.append(scanner)
    
    def _add_result(self, key: str, value: Any) -> None:
        """Add a result to the results dictionary (thread-safe).
        
        Args:
            key: Scanner name
            value: Scanner result
        """
        with self._lock:
            self._results[key] = value
    
    def _add_error(self, key: str, error: Exception) -> None:
        """Add an error to the errors dictionary (thread-safe).
        
        Args:
            key: Scanner name
            error: Exception that occurred
        """
        with self._lock:
            self._errors[key] = error
    
    def scan(
        self, 
        number: Number, 
        options: Optional[ScannerOptions] = None
    ) -> Tuple[Dict[str, Any], Dict[str, Exception]]:
        """Run all scanners on a phone number.
        
        Args:
            number: Phone number to scan
            options: Scanner options
            
        Returns:
            Tuple[Dict[str, Any], Dict[str, Exception]]: Results and errors
        """
        if options is None:
            options = ScannerOptions()
        
        # Reset results and errors
        self._results = {}
        self._errors = {}
        
        # Run scanners concurrently
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {}
            
            for scanner in self._scanners:
                future = executor.submit(self._run_scanner, scanner, number, options)
                futures[future] = scanner
            
            # Wait for all scanners to complete
            for future in as_completed(futures):
                scanner = futures[future]
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"Unexpected error in scanner {scanner.name()}: {e}")
                    self._add_error(scanner.name(), e)
        
        return self._results, self._errors
    
    def _run_scanner(
        self, 
        scanner: Scanner, 
        number: Number, 
        options: ScannerOptions
    ) -> None:
        """Run a single scanner (called in thread pool).
        
        Args:
            scanner: Scanner to run
            number: Phone number to scan
            options: Scanner options
        """
        try:
            # Check if scanner should run
            err = scanner.dry_run(number, options)
            if err is not None:
                logger.debug(
                    f"Scanner {scanner.name()} was ignored because it should not run: {err}"
                )
                return
            
            # Run the scanner
            data = scanner.run(number, options)
            if data is not None:
                self._add_result(scanner.name(), data)
        
        except Exception as e:
            logger.debug(f"Scanner {scanner.name()} failed: {e}")
            self._add_error(scanner.name(), e)
    
    def get_all_scanners(self) -> List[Scanner]:
        """Get all registered scanners.
        
        Returns:
            List[Scanner]: List of all scanners
        """
        return self._scanners.copy()
    
    def get_scanner(self, name: str) -> Optional[Scanner]:
        """Get a scanner by name.
        
        Args:
            name: Scanner name
            
        Returns:
            Optional[Scanner]: Scanner instance or None if not found
        """
        for scanner in self._scanners:
            if scanner.name() == name:
                return scanner
        return None
