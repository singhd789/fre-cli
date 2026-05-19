'''
entry point for fre run subcommands
'''

import click
from fre.run import generate_srun_script

@click.group(help=click.style(" - run subcommands", fg=(164,29,132)))
def run_cli():
    ''' entry point to fre run click commands '''

@run_cli.command()
@click.option('-y',
              '--yamlfile',
              help = "")
@click.option('-e',
              '--experiment',
              multiple = True,
              help = "")
@click.option('-s',
              '--submit',
              is_flag=True,
              help = "")
def gen_srun(yamlfile, experiment, submit):
    """
    """
    generate_srun_script.gen_srun_subtool(yamlfile, experiment, submit)
