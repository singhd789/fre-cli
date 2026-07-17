"""
List_yamls_script provides methods to list and return YAML configurations to be combined into
one, resolved configuration. Different click options are avaiable to return only relevant yamls
depending on the process the user wants to run (compile, runtime, postprocess, analysis).
"""
import logging
from pathlib import Path
import yaml

fre_logger = logging.getLogger(__name__)

def list_yamls_subtool(yamlfile: str, experiment: str, compile_only: bool, runtime_only: bool,
                       postprocess_only: bool, analysis_only: bool):
    """
    List_yamls_subtool lists the relevant yamls to combine. The default list returned is ALL yamls
    associated with an experiment. (model, compile, platforms, settings, runtime, postprocessing,
    analysis yamls)

    :param yamlfile: is the path to the model yaml configuration file
    :type yamlfile: str
    :param experiment: is the name of the experiment
    :type experiment: str
    :param compile_only: is the flag to pass yaml configurations needed for compilation
    :type compile_only: boolean 
    :param runtime_only: is the flag to pass yaml configurations needed for model runtime
    :type runtime_only: boolean 
    :param postprocess_only: is the flag to pass yaml configurations needed for postprocessing
    :type postprocess_only: boolean 
    :param analysis_only: is the flag to pass yaml configurations needed for postprocessing
    :type analysis_only: boolean
    :return: Space separated string of absolute paths to yaml configurations
    :rtype: str
    """
    model_yaml = Path(yamlfile).name
    model_yaml_path = Path(yamlfile).resolve().parent

    exp_name = experiment
    with open(yamlfile, 'r', encoding="utf-8") as yf:
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

    yamls_full_path = ""
    # Add full path for yaml configurations
    for y in yamls:
        yamls_full_path += f"{str(model_yaml_path)}/{y} "

    # set logger level to INFO
    former_log_level = fre_logger.level
    fre_logger.setLevel(logging.INFO)

    fre_logger.info("YAMLS to be combined (Experiment => %s):", experiment)
    for y in yamls_full_path.split():
        fre_logger.info("  - %s", y)

    fre_logger.setLevel(former_log_level)

    # Check if the paths exist; give warning
    fre_logger.warning("")
    for y in yamls_full_path.split():
        if not Path(y).exists():
            fre_logger.warning("**DNE**: %s", y)
    fre_logger.warning("")

    return yamls_full_path
