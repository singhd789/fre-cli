"""
YAML Combination Utilities for FRE
----------------------------------

This module provides utility functions for combining model, experiment, compile, platform, and analysis
YAML files into unified configurations for the Flexible Runtime Environment (FRE) workflow. It offers routines
to consolidate YAMLs for CMORization, compilation, and post-processing, supporting both command-line tools
and internal workflow automation.
"""

import os
import yaml
import logging
from pathlib import Path
from pprint import pformat
import pprint
from typing import Optional, Union, Any, Dict

from fre.yamltools.helpers import output_yaml, check_fre_version, clean_yaml

from uwtools.api import config
from uwtools.api.logging import use_uwtools_logger
#>>> use_uwtools_logger()
import yaml
from fre.list_.list_yamls_script import list_yamls_subtool 

fre_logger = logging.getLogger(__name__)

def yamltools_combine_subtool(yamlfile:str, experiment:str, platform:str,
                         target:str, output: Optional[str]=None) -> dict:
    """
    Depending on `use` argument passed, either create the final
    combined yaml for compilation or post-processing

    :param yamlfile: Path to the model YAML configuration
    :type yamlfile: str
    :param experiment: Post-processing experiment name
    :type experiment: str
    :param platform: Platform name to be used
    :type platform: str
    :param output: Output file name
    :type output: str
    :raise ValueError: if 'use' value is not a valid entry (compile, pp or cmor)
    :return: yaml dictionary containing combined information from multiple yaml configurations
    :rtype: dict

    ..note:: The output file name should include a .yaml extension to indicate
             it is a YAML configuration file
    """
    # Check fre_cli_version compatibility before any YAML combining
    fre_logger.info('checking fre_cli_version compatibility...')
    check_fre_version(yamlfile)

    YAMS = []
    init = {"name": experiment, "platform": platform, "target": target}

    # create intermediate yaml to pass to uw config compose
    #  - needs yamls files; cannot pass dictionaries
    #  - will be removed later
    init_file = f"{Path.cwd()}/{output}"
    output_yaml(init, init_file)

## LIST YAMLS ##
    # list yamls to combine
    ytc = list_yamls_subtool(yamlfile, experiment)

    ## append init file (needed for schema and other variables?)
    YAMS.append(init_file)

    ## append list of yamls
    YAMS.extend(ytc)

## COMBINE YAMLS AND RESOLVE WHERE WE CAN ##
    ## uw config compose: pass yaml list to compose final yaml
    # CAN THIS BE DICTIONARIES??
    # config.compose returns a base class specifying methods to read, manipulate,
    # and write several configuration-file formats. (use as_dict to return dictionary)
    combined_yaml_dict = config.compose(configs=YAMS, realize=True).as_dict()

## CLEAN SERIALIZED YAML ##
    cleaned_yaml_dict = clean_yaml(combined_yaml_dict)
    if not cleaned_yaml_dict:
        raise ValueError("YAML configuration could not be cleaned (experiments)")

## CATCH UNRESOLVED AND OUTPUT ##
    ## uw config realize: resolve final yaml
    ## cant add values_needed=True or else the variables won't render???
    use_uwtools_logger()
    try:
        if output:
            fre_logger.info("Writing resolved YAML file: %s", init_file)
            final_dict = config.realize(input_config = cleaned_yaml_dict,
                                        total = True,
                                        output_file = init_file)
        else:
            fre_logger.info("Resolved YAML saved as dictionary")
            final_dict = config.realize(input_config = cleaned_yaml_dict,
                                        total = True)
            # clean init_file
            Path(init_file).unlink()
    except:
#        fre_logger.info("COULD NOT WRITE FILE; COULD NOT RESOLVE, DO NOT PASS GO")
        config.realize(input_config = cleaned_yaml_dict,
                       values_needed = True)
        raise ValueError("COULD NOT WRITE FILE; COULD NOT RESOLVE, DO NOT PASS GO")


# VALIDATE SERIALIZED YAML ##
    ## uw config validate
    # output from validate is True or False
    validate_out = config.validate(schema_file="/home/Dana.Singh/fre/singh/generalize-yaml-serialization/fre/gfdl_msd_schemas/FRE/fre_make.json",
                                   config_data=cleaned_yaml_dict)

    if validate_out:
        fre_logger.info("VALID")
    else:
        fre_logger.error("INVALID")
        raise ValueError("INVALID. CHECK YA YAMLS")
