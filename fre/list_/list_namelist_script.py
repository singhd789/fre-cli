"""
Notes: some input nml are in a string block because they might be different across experiments
also some have inheritance that include other experiment's namelist files

"""

from pathlib import Path
import logging
import textwrap
from fre.yamltools import combine_yamls_script as cy
from fre.yamltools import helpers

fre_logger = logging.getLogger(__name__)

def list_namelist_subtool(yamlfile: str, experiment: None):
    """
    List the namelist files associated with the experiment name

    :param yamlfile: path to the yaml configuration file
    :type yamlfile: str
    :param experiment: Name of experiment
    :type experiment: str
    """
    # set logger level to INFO
    former_log_level = fre_logger.level
    fre_logger.setLevel(logging.INFO)

    exp = experiment
    platform = None
    target = None

#    # Combine model / experiment
#    yml_dict = cy.consolidate_yamls(yamlfile = yamlfile,
#                                    experiment = experiment,
#                                    platform = platform,
#                                    target = target,
#                                    use = "compile",
#                                    output = None)
#
#    # Validate the yaml
#    fre_pkg_dir = Path(__file__).resolve().parents[1]
#    schema_path = f"{fre_pkg_dir}/gfdl_msd_schemas/FRE/fre_make.json"
#    # from fre.yamltools
#    helpers.validate_yaml(yml_dict, schema_path)

    yml = helpers.yaml_load(yamlfile) 
    fre_logger.info("Namelist files associated with %s:", experiment)
    run = yml.get("run")

    nml_list = []
    for k,v in run.get("input").get("namelist").items():
        if k !="common_files":
            tmp_nml = Path(f"{Path.cwd()}/tmp_nml")
            Path(tmp_nml).mkdir(parents=True, exist_ok=True)

            with open(f"{tmp_nml}/{k}.nml", "w") as f:
                f.write(f" &{k}\n")
                for line in v.splitlines():
                    f.write(f"  {line}\n")
                f.write("/")

            nml_list.append(Path(f"{tmp_nml}/{k}.nml"))

####QUESTIONS
# are there namelist files for each experiment?
# some are inherited...hm
####

####IDEA
# is this too much?
# create "tmp" location and write nml files based of strings defined in yaml
# then all that would be passed is file paths to uw tools
# should uw tools/yamltools clean tmp location?
####
    # get files listed
        elif k == "common_files":
            nml_list.extend(run.get("input").get("namelist").get("common_files"))

    for i in nml_list:
        fre_logger.info('    - %s', i)
    fre_logger.info("")
    fre_logger.setLevel(former_log_level)

    return nml_list
