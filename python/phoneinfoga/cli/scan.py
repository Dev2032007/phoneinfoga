"""Scan command for scanning phone numbers."""

import logging
import sys
import click
from colorama import Fore, Style
from dotenv import load_dotenv

from phoneinfoga.lib.number import Number, is_valid
from phoneinfoga.lib.filter import Engine
from phoneinfoga.lib.remote import Library, init_scanners, ScannerOptions
from phoneinfoga.lib.output import get_output, OutputType
from .root import cli, exit_with_error

logger = logging.getLogger(__name__)


@cli.command()
@click.option(
    "-n", "--number",
    required=True,
    help="The phone number to scan (E164 or international format)"
)
@click.option(
    "-D", "--disable",
    multiple=True,
    help="Scanner to skip for this scan"
)
@click.option(
    "--plugin",
    multiple=True,
    help="Extra scanner plugin to use for the scan"
)
@click.option(
    "--env-file",
    multiple=True,
    help="Env files to parse environment variables from"
)
def scan(number: str, disable: tuple, plugin: tuple, env_file: tuple) -> None:
    """Scan a phone number.
    
    Example: phoneinfoga scan -n +33678342311
    """
    # Load environment files
    for env_path in env_file:
        load_dotenv(env_path)
    if not env_file:
        load_dotenv()  # Load default .env if exists
    
    click.echo(f"{Style.BRIGHT}Running scan for phone number {number}...{Style.RESET_ALL}\n")
    
    # Validate phone number
    if not is_valid(number):
        logger.debug(f"Input phone number is invalid: {number}")
        exit_with_error(Exception("Given phone number is not valid"))
    
    # Parse phone number
    try:
        num = Number(number)
    except Exception as e:
        exit_with_error(e)
    
    # Load plugins
    for plugin_path in plugin:
        try:
            from phoneinfoga.lib.remote.scanner import open_plugin
            open_plugin(plugin_path)
        except Exception as e:
            exit_with_error(e)
    
    # Initialize filter and library
    filter_engine = Engine()
    filter_engine.add_rule(*disable)
    
    library = Library(filter_engine)
    init_scanners(library)
    
    # Run scan
    results, errors = library.scan(num, ScannerOptions())
    
    # Output results
    output = get_output(OutputType.CONSOLE, sys.stdout)
    output.write(results, errors)
