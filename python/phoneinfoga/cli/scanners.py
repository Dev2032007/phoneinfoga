"""Scanners command for listing available scanners."""

import click

from phoneinfoga.lib.filter import Engine
from phoneinfoga.lib.remote import Library, init_scanners
from .root import cli, exit_with_error


@cli.command()
@click.option(
    "--plugin",
    multiple=True,
    help="Extra scanner plugin to load"
)
def scanners(plugin: tuple) -> None:
    """Display list of loaded scanners.
    
    Example: phoneinfoga scanners
    """
    # Load plugins
    for plugin_path in plugin:
        try:
            from phoneinfoga.lib.remote.scanner import open_plugin
            open_plugin(plugin_path)
        except Exception as e:
            exit_with_error(e)
    
    # Initialize library
    library = Library(Engine())
    init_scanners(library)
    
    # Display scanners
    all_scanners = library.get_all_scanners()
    for i, scanner in enumerate(all_scanners):
        click.echo(f"{scanner.name()}")
        click.echo(f"{scanner.description()}")
        if i < len(all_scanners) - 1:
            click.echo()
