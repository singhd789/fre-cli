''' fre lister '''

#import logging
#fre_logger = logging.getLogger(__name__)

import click
from fre.list_ import list_experiments_script
from fre.list_ import list_platforms_script
from fre.list_ import list_pp_components_script
from fre.list_ import list_tables_script

@click.group(help=click.style(" - list subcommands", fg=(232,204,91)))
def list_cli():
    ''' entry point to fre list click commands '''

@list_cli.command()
@click.option("-y",
              "--yamlfile",
              type=str,
              help="Model YAML configuration file",
              required=True)
def exps(yamlfile):
    """ - List experiments  available"""
    list_experiments_script.list_experiments_subtool(yamlfile)

@list_cli.command()
@click.option("-y",
              "--yamlfile",
              type=str,
              help="Model YAML configuration file",
              required=True)
def platforms(yamlfile):
    """ - List platforms available """
    list_platforms_script.list_platforms_subtool(yamlfile)

@list_cli.command()
@click.option("-y",
              "--yamlfile",
              type=str,
              help="Model YAML configuration file",
              required=True)
@click.option("-e",
              "--experiment",
              type=str,
              help="Experiment to be post-processed",
              required=True)
def pp_components(yamlfile, experiment):
    """ - List components to be ppst-processed for a defined experiment"""
    list_pp_components_script.list_ppcomps_subtool(yamlfile, experiment)

@list_cli.command()
@click.option("-y",
              "--yamlfile",
              type=str,
              help="Model YAML configuration file",
              required=True)
@click.option("--diag-tables",
              is_flag = True,
              help="True/False option to list diag tables")
@click.option("--data-tables",
              is_flag = True,
              help="True/False option to list data tables")
@click.option("--field-tables",
              is_flag = True,
              help="True/False option to list field tables")
@click.option("--all",
              "all_tables",
              is_flag = True,
              help="True/False option to list field tables")
def tables(yamlfile, diag_tables, data_tables, field_tables, all_tables):
    """ - List diag, field, and data tables available """
    list_tables_script.list_tables_subtool(yamlfile, diag_tables, data_tables, field_tables, all_tables)
