"""
Generate the srun command to run the executable
"""
import logging
import subprocess
import yaml
from pathlib import Path

# set up logging
fre_logger = logging.getLogger(__name__)

def srun_coupled(info):
    """
    Generate srun command if running coupled or not
    """
    cmd = "srun "

    ## ATM RANKS SHOULD ALWAYS BE DEFINED
    atm_ranks = info.get("atm").get("ranks")
    atm_threads = info.get("atm").get("threads")

    # IF NOT COUPLED
    ntasks = f"--ntasks={atm_ranks}"
    cpus = f"--cpus-per-task={atm_threads}"
    export = f"--export=ALL,OMP_NUM_THREADS={atm_threads}"
    executable_path = "[executable/path]"
    cmd1 = f"{ntasks} {cpus} {export} {executable_path}"

    # IF COUPLED
    ocn_ranks = info.get("ocn").get("ranks")
    ocn_threads = info.get("ocn").get("threads")
    cmd2 = ""
    if ocn_ranks and ocn_threads:
        ntasks = f"--ntasks={ocn_ranks}"
        cpus = f"--cpus-per-task={ocn_threads}"
        export = f"--export=ALL,OMP_NUM_THREADS={ocn_threads}"
        executable_path = "[executable/path]"
        cmd2 += f"{ntasks} {cpus} {export} {executable_path}"

    cmd += f"{cmd1}"
    if cmd2:
        cmd += f" : {cmd2}"

    return cmd

class GenSRUN():
    """
    Class holding routines for extracting information to compose the srun
    command that will run the model executable.

    :ivar str yamlfile:
    :ivar str experiment:
    :ivar bool submit:
    """
    def __init__(self, yamlfile, experiment, submit):
        """
        Initialize the object.
        """
        self.yaml = yamlfile
        self.exp = experiment #(there can be multiple)
        self.submit = submit

    def load_yaml(self):
        """
        Load the resolved yamlfile.
        """
        with open(self.yaml, 'r', encoding="utf-8") as yf:
            y = yaml.load(yf, Loader=yaml.Loader)
        return y

    def get_layout_info(self, yml):
        """
        Save the layout information associated with the experiment
        name passed.
        """
        #self.exp to get relevant info
        #create or save [{self.exp: info}, ...]
        layout_info = []
        for e in self.exp:
            if e not in yml["layouts"]:
                raise ValueError("Experiment not defined in the layouts.yaml!!")

            valid_layout = {e: yml["layouts"].get(e)}
            layout_info.append(valid_layout)

        return layout_info

    def compose_srun(self, layout_info_list):
        """
        Generate the srun command and print.
        """
        cmds_generated = []
        #if more than one experiment
        if len(layout_info_list) > 1:
            fre_logger.info("*** More than one experiment passed ***")
            for layout in layout_info_list:
                for e in self.exp:
                    if layout.get(e):
                        info = layout[e]
                        cmd = srun_coupled(info)
                        cmds_generated.append(cmd)
                        fre_logger.info("For %s: %s", e, cmd)
        else:
            layout = layout_info_list[0]
            info = layout[self.exp[0]]
            cmd = srun_coupled(info)
            cmds_generated.append(cmd)
            fre_logger.info("For %s: %s", self.exp[0], cmd)

        return cmds_generated

## Actual fre-cli subtool call
def gen_srun_subtool(yamlfile, experiment, submit):
    """
    Actual subtool to do the thing
    """
    # initialize object
    srun_obj = GenSRUN(yamlfile, experiment, submit)
    if isinstance(yamlfile, dict):
        yaml_dict = yamlfile
    else:
        yaml_dict = srun_obj.load_yaml()
    layout_info_list = srun_obj.get_layout_info(yaml_dict)
    srun_cmd = srun_obj.compose_srun(layout_info_list)

    if submit:
        for cmd in srun_cmd:
            # for better security (so we don't have to use shell=True), split the string
            cmd_args = cmd.split()
            fre_logger.info("*** Running the executable ***")
            subprocess.run(cmd_args, check=True)
    else:
        fre_logger.info("To run the srun command, pass -s or --submit")
