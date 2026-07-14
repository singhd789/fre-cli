'''
entry point for fre run subcommands
'''

import click
from fre.run import input_stager_script

@click.group(help=click.style(" - run subcommands", fg=(164,29,132)))
def run_cli():
    ''' entry point to fre run click commands '''

@run_cli.command()
@click.option("-ds",
              "--datasets",
              type = list,
              help = "Comma-separated list")
@click.option("-nml",
              "--namelists",
              type = list,
              help = "Comma-separated list")
@click.option("-tb",
              "--tables",
              type = list,
              help = "Comma-separated list")
@click.option("-wd", 
              "--workdir",
              type = list,
              help = "Path")
def input_stager(datasets, namelists, tables, workdir):
   """ - Set up the workdir in preparation for running the model """
   input_stager_script.input_stager_subtool(datasets, namelists, tables, workdir)
