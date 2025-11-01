"""Phone number class and parsing."""

from dataclasses import dataclass
from typing import Optional
import phonenumbers
from phonenumbers import carrier, geocoder

from .utils import format_number, parse_country_code


@dataclass
class Number:
    """Represents a parsed phone number with metadata.
    
    Attributes:
        valid: Whether the phone number is valid
        raw_local: Raw local format without formatting
        local: Local format with formatting
        e164: E.164 format (international standard)
        international: International format without + prefix
        country_code: Numeric country calling code
        country: ISO country code
        carrier: Carrier name (if available)
    """
    
    valid: bool
    raw_local: str
    local: str
    e164: str
    international: str
    country_code: int
    country: str
    carrier: str
    
    def __init__(self, number: str):
        """Initialize a Number from a phone number string.
        
        Args:
            number: Phone number in E164 or international format
            
        Raises:
            phonenumbers.NumberParseException: If the number cannot be parsed
        """
        # Format the number and ensure it starts with +
        formatted = '+' + format_number(number)
        country = parse_country_code(formatted)
        
        # Parse the number
        parsed = phonenumbers.parse(formatted, country)
        
        # Extract all information
        self.valid = phonenumbers.is_valid_number(parsed)
        
        # Get national format and extract raw version
        national_format = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
        self.raw_local = format_number(national_format)
        self.local = national_format
        
        # Get E164 and international formats
        self.e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        self.international = format_number(self.e164)
        
        # Get country code and country
        self.country_code = parsed.country_code
        self.country = country
        
        # Get carrier information
        self.carrier = carrier.name_for_number(parsed, "en") or ""
    
    def to_dict(self) -> dict:
        """Convert the Number to a dictionary.
        
        Returns:
            dict: Dictionary representation of the Number
        """
        return {
            "valid": self.valid,
            "raw_local": self.raw_local,
            "local": self.local,
            "e164": self.e164,
            "international": self.international,
            "country_code": self.country_code,
            "country": self.country,
            "carrier": self.carrier,
        }
    
    def __str__(self) -> str:
        """String representation of the Number.
        
        Returns:
            str: E164 format of the number
        """
        return self.e164
