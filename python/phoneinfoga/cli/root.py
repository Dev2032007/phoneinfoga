"""Root CLI command and main entry point."""

import sys
import click
from colorama import Fore, Style

from phoneinfoga.logs import init_logging


@click.group()
@click.version_option()
def cli() -> None:
    """PhoneInfoga - Advanced information gathering & OSINT tool for phone numbers.
    
    PhoneInfoga is one of the most advanced tools to scan phone numbers 
    using only free resources.
    """
    pass


def exit_with_error(error: Exception) -> None:
    """Exit the program with an error message.
    
    Args:
        error: Exception to display
    """
    click.echo(f"{Fore.RED}{str(error)}{Style.RESET_ALL}", err=True)
    sys.exit(1)


def main() -> None:
    """Main entry point for the CLI."""
    init_logging()
    
    # Import commands to register them
    from . import scan, serve, version, scanners
    
    try:
        cli()
    except Exception as e:
        exit_with_error(e)


if __name__ == "__main__":
    main()
