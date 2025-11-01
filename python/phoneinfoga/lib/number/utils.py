"""Utility functions for phone number handling."""

import re
from typing import Optional


def format_number(number: str) -> str:
    """Format a phone number to remove unnecessary chars.
    
    Removes all non-digit characters from the phone number.
    
    Args:
        number: Phone number string to format
        
    Returns:
        str: Formatted phone number containing only digits
    """
    return re.sub(r'[_\W]+', '', number)


def parse_country_code(number: str) -> str:
    """Parse a phone number and return ISO country code.
    
    This uses the phonenumbers library to detect the country code.
    
    Args:
        number: Phone number string to parse
        
    Returns:
        str: ISO country code (e.g., "US", "FR", "GB")
    """
    import phonenumbers
    from phonenumbers import geocoder
    
    try:
        formatted = format_number(number)
        if not formatted.startswith('+'):
            formatted = '+' + formatted
        
        parsed = phonenumbers.parse(formatted, None)
        country_code = geocoder.region_code_for_number(parsed)
        return country_code if country_code else ""
    except Exception:
        return ""


def is_valid(number: str) -> bool:
    """Check if a phone number has a valid format.
    
    Args:
        number: Phone number string to validate
        
    Returns:
        bool: True if the number contains only digits (after formatting)
    """
    formatted = format_number(number)
    return bool(re.match(r'^[0-9]+$', formatted))
