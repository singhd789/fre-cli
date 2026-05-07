'''
entry point for fre run subcommands
'''

import click
from .frerunexample import run_test_function
from fre.run import configure_ascii_script

@click.group(help=click.style(" - run subcommands !!!NotImplemented!!!", fg=(164,29,132)))
def run_cli():
    ''' entry point to fre run click commands '''

@run_cli.command()
@click.option('--uppercase', '-u', is_flag=True, help = 'Print statement in uppercase.')
def function(uppercase):
    """ - Execute fre run test """
    run_test_function(uppercase)
    raise NotImplementedError('fre run has not been implemented yet!')

@run_cli.command()
@click.option('--uppercase', '-u',
              is_flag=True,
              help = "")
def configure_ascii():
    """
    """
    configure_ascii_script.configure_ascii_subtool()
