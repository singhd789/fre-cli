''' fre lister '''

#import logging
#fre_logger = logging.getLogger(__name__)

import click
from fre.list_ import list_experiments_script
from fre.list_ import list_platforms_script
from fre.list_ import list_pp_components_script
from fre.list_ import list_yamls_script

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
    """ - List components to be post-processed for a defined experiment"""
    list_pp_components_script.list_ppcomps_subtool(yamlfile, experiment)

@list_cli.command()
@click.option("-y",
              "--yamlfile",
              type=str,
              help="Model YAML configuration file",
              required=True)
@click.option("-e",
              "--experiment",
              type=str,
              help="Experiment name")
@click.option("--compile-only",
              type=bool,
              is_flag=True,
              default = False,
              help="List yaml configuration files needed for compilation, defined in "
                    "the `[model].yaml`. This includes the model, platform, and compile "
                    "configuration files.")
@click.option("--runtime-only",
              type=bool,
              is_flag=True,
              default = False,
              help="List yaml configuration files needed for model runtime, defined in "
                    "the `[model].yaml`.")
@click.option("--postprocess-only",
              type=bool,
              is_flag=True,
              default = False,
              help="List yaml configuration files needed for postprocessing, defined in "
                    "the `[model].yaml`.")
@click.option("--analysis-only",
              type=bool,
              is_flag=True,
              default = False,
              help="List yaml configuration files needed for analysis, defined in "
                    "the `[model].yaml`.")
def yamls(yamlfile, experiment, compile_only, runtime_only, postprocess_only, analysis_only):
    """ - List yamls to be combined"""
    list_yamls_script.list_yamls_subtool(yamlfile, experiment, compile_only, runtime_only, postprocess_only, analysis_only)
