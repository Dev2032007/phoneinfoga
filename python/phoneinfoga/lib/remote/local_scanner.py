"""Local scanner for basic phone number information."""

from dataclasses import dataclass
from typing import Optional

from phoneinfoga.lib.number import Number
from .scanner import Scanner, ScannerOptions


@dataclass
class LocalScannerResponse:
    """Response from the local scanner."""
    
    raw_local: str
    local: str
    e164: str
    international: str
    country_code: int
    country: str
    carrier: str


class LocalScanner(Scanner):
    """Scanner that provides basic local phone number information."""
    
    def name(self) -> str:
        """Get the scanner name."""
        return "local"
    
    def description(self) -> str:
        """Get the scanner description."""
        return "Provides basic phone number information from local parsing"
    
    def dry_run(self, number: Number, options: ScannerOptions) -> Optional[Exception]:
        """Check if the scanner should run.
        
        The local scanner always runs.
        """
        return None
    
    def run(self, number: Number, options: ScannerOptions) -> LocalScannerResponse:
        """Run the local scanner.
        
        Args:
            number: Phone number to scan
            options: Scanner options
            
        Returns:
            LocalScannerResponse: Basic phone number information
        """
        return LocalScannerResponse(
            raw_local=number.raw_local,
            local=number.local,
            e164=number.e164,
            international=number.international,
            country_code=number.country_code,
            country=number.country,
            carrier=number.carrier,
        )
