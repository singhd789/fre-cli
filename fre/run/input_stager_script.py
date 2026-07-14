"""
Input_stager_script provides methods to copy/move required files into
a working directory in preparation for the model run. 

These files include data, diag, and field tables, necessary input datasets,
namelist files, and the model container or executable. 
"""
from pathlib import Path
import logging
import shutil

fre_logger = logging.getLogger(__name__)

class StageInput():
    """ 
    Class holding routines for copying necessary input files into a
    working directory in preparation for a model run. 

    :ivar str yamlfile: Path to the model yaml configuration
    :ivar str experiment: Post-processing experiment name
    :ivar str platform: Platform name
    :ivar str target: Target name
    """
    def __init__(self, datasets, namelists, tables, workdir):
        self.ds = datasets.split(',')
        self.nml = namelists.split(',')
        self.tb = tables.split(',')
        self.wd = Path(workdir).resolve()

        # set up/create workdir (absolute path)
        if not self.wd.exists():
            self.wd.mkdir(exist_ok=True, parents=True)
            fre_logger.info("Working directory created: %s", self.wd)
        else:
            fre_logger.info("what am I? Chopped liver?")

    def stage_datasets(self):
        """
        Stage_datasets loops over a list of input datasets associated with
        an experiment and copies the files to the work directory.

        :param self: is the instance of the class StageInput
        :type self: class
        """
        for d in self.ds:
            shutil.copy(d, self.wd)
        fre_logger.info("%s datasets to be added to workdir (%s)", len(ds), self.wd)

    def stage_namelist(self):
        """
        Stage_namelists loops over a list of input namelists associated with
        an experiment and copies the files to the work directory.

        :param self: is the instance of the class StageInput
        :type self: class
        """
        for n in self.nml:
            shutil.copy(n, self.wd)
        fre_logger.info("%s namelists to be added to workdir (%s)", len(nml), wd)

    def stage_tables(self):
        """
        Stage_tables loops over a list of diag, data, and field tables associated
        with an experiment and copies the files to the work directory.

        :param self: is the instance of the class StageInput
        :type self: class
        """
        #wondering if we should combine here as well
        for t in self.tb:
            shutil.copy(t, self.wd)

        fre_logger.info("%s tables to be added to workdir (%s)", len(tables), wd)

def input_stager_subtool(datasets, namelists, tables, workdir):
    """
    Input_stager ingests lists of input datasets, tables, and namelists extracted from
    a resolved runtime YAML configuration file and copies the relevant files associated
    with a model run into the given working directory. 

    :param datasets: is the list of input datasets associated with the model run
    :type datasets: list
    :param namelists: is the list of namelist files associated with the model run
    :type namelists: list
    :param tables: is the list of diag, data, and field tables associated with the model run 
    :type tables: list
    :param workdir:
    :type workdir: str
    """
    ah = StageInput(datasets, namelists, tables, workdir)
    ah.stage_datasets()
    ah.stage_namelists()
    ah.stage_tables()

    ##if we were passing in a yaml file that had the structure defined in uw tools docs --> or could do this: uw fs copy --target-dir [dir] --config-file [resolved] --key-path run..... THEY WOULD ALL HAVE TO BE LISTED UNDER THE SAME FILES SECTION THOUGH - is that possible? (datasets and namelists, yes maybe, tables?, container? executable?
#### CREATE EXAMPLE YAML WITH THIS STRUCTURE DANA
