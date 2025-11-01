"""Version command for displaying version information."""

import click

from phoneinfoga.build import get_version_string
from .root import cli


@cli.command()
def version() -> None:
    """Print current version of the tool.
    
    Example: phoneinfoga version
    """
    click.echo(f"PhoneInfoga {get_version_string()}")
