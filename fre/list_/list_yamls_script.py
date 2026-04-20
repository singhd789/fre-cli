"""
"""
import logging
import yaml
import pprint
from pathlib import Path

fre_logger = logging.getLogger(__name__)

def list_yamls_subtool(yamlfile: str, experiment: str):
    """
    List the relevant yamls to combine

    :param yamlfile: Path to the model yaml configuration file
    :type yamlfile: str
    :param experiment: Name of the experiment
    :type experiment: str
    """
    model_yaml = Path(yamlfile).name
    model_yaml_path = Path(yamlfile).resolve().parent

    exp_name = experiment
    with open(yamlfile, 'r') as yf:
        yaml_dict = yaml.load(yf, Loader = yaml.Loader)

    compile_data = yaml_dict["build"].get("compileYaml").split("/")[-1]
    platform_data = yaml_dict["build"].get("platformYaml").split("/")[-1]
    exp_data = yaml_dict["experiments"].get(exp_name)
    yamls = [model_yaml, compile_data, platform_data]

    # list yamls associated with the run, post-processing, and analysis
    if exp_name:
        for value in exp_data.values():
            if isinstance(value, list):
                yamls.extend(value)
            else:
                yamls.append(value)
    else:
        fre_logger.info("No experiment name passed. Will only provide YAMLs related to compilation.")

    # Add full path for yaml configurations
    yamls_full_path = [f"{str(model_yaml_path)}/"+y for y in yamls]

    # set logger level to INFO
    former_log_level = fre_logger.level
    fre_logger.setLevel(logging.INFO)

    fre_logger.info("YAMLS to be combined (%s):", experiment)
    for y in yamls_full_path:
        fre_logger.info("  - %s", y)

    fre_logger.setLevel(former_log_level)

    return yamls_full_path
