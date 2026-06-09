"""
"""
import logging
import yaml
import pprint
from pathlib import Path

fre_logger = logging.getLogger(__name__)

def list_yamls_subtool(yamlfile: str, experiment: str, compile_only: bool, runtime_only: bool, postprocess_only: bool, analysis_only: bool):
    """
    List the relevant yamls to combine. The default list returned is ALL yamls.
    (model, compile, platforms, settings, runtime, postprocessing, analysis yamls)

    :param yamlfile: Path to the model yaml configuration file
    :type yamlfile: str
    :param experiment: Name of the experiment
    :type experiment: str
    :param compile_only: Flag to only pass yaml configs needed for compilation
    :type compile_only: boolean 
    :param runtime_only: Flag to only pass yaml configs needed for model runtime
    :type runtime_only: boolean 
    :param postprocess_only: Flag to only pass yaml configs needed for postprocessing
    :type postprocess_only: boolean 
    :param analysis_only: Flag to only pass yaml configs needed for postprocessing
    :type analysis_only: boolean 
    """
    model_yaml = Path(yamlfile).name
    model_yaml_path = Path(yamlfile).resolve().parent

    exp_name = experiment
    with open(yamlfile, 'r') as yf:
        yaml_dict = yaml.load(yf, Loader = yaml.Loader)

    compile_data = yaml_dict["build"].get("compileYaml").split("/")[-1]
    platform_data = yaml_dict["build"].get("platformYaml").split("/")[-1]
    exp_data = yaml_dict["experiments"].get(exp_name)

    yamls = [model_yaml]
    # list yamls associated with the compile, run, post-processing, and analysis
    if exp_name:
        settings_data = exp_data["settings"]

        if compile_only:
            yamls.extend([compile_data, platform_data])
        elif runtime_only:
            yamls.extend([platform_data, settings_data])
            yamls.extend(exp_data["run"])
        elif postprocess_only and not analysis_only:
            yamls.append(settings_data)
            yamls.extend(exp_data["postprocess"])
        elif analysis_only and not postprocess_only:
            yamls.append(settings_data)
            yamls.extend(exp_data["analysis"])
        elif postprocess_only and analysis_only:
            yamls.append(settings_data)
            yamls.extend(exp_data["postprocess"])
            yamls.extend(exp_data["analysis"])
        else: # list all yamls - default behavior
            yamls.extend([compile_data, platform_data])
            for value in exp_data.values():
                if isinstance(value, list):
                    yamls.extend(value)
                else:
                    yamls.append(value)
    else:
        fre_logger.info("No experiment name passed. Will only provide YAMLs related to compilation.")
        yamls.extend([compile_data, platform_data])

    # Add full path for yaml configurations
    yamls_full_path = [f"{str(model_yaml_path)}/"+y for y in yamls]

    # set logger level to INFO
    former_log_level = fre_logger.level
    fre_logger.setLevel(logging.INFO)

    fre_logger.info("YAMLS to be combined (Experiment => %s):", experiment)
    for y in yamls_full_path:
        fre_logger.info("  - %s", y)

    fre_logger.setLevel(former_log_level)

    return yamls_full_path
