"""
"""
import logging

# set up logging
fre_logger = logging.getLogger(__name__)


class Gen_SRUN() 
    def __init__(yamlfile, experiment, submit):
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

    def get_layout_info(yaml):
        """
        Save the layout information associated with the experiment
        name passed.
        """

    def compose_srun_cmd(layout_yaml_dict):
        """
        Generate the srun command and print.
        """

    def run_srun():
        """
        Run the srun command if -s, --submit is passed
        """

## Actual fre-cli subtool call
def gen_srun()
    """
    """
    # initialize object
    srun_obj = Gen_SRUN(yamlfile, experiment, submit)
    yaml_dict = srun_obj.load_yaml()
    layout_info = srun_obj.get_layout_info(yaml_dict)
    srun_cmd = srun_obj.compose_srun_cmd(layout_info)

    fre_logger.info("Generated srun commmand: %s", srun_cmd)
    fre_logger.info("To run the srun command, pass -s or --submit")
