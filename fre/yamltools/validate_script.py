"""
"""
import logging
import subprocess
from pathlib import Path
from typing import Union
from tempfile import TemporaryDirectory
from uwtools.api import config
from uwtools.api.logging import use_uwtools_logger
from fre.yamltools import helpers

fre_logger = logging.getLogger(__name__)

class ValidateYaml():
    """
    """
    def __init__(self, yaml, json_schema, application):
        """

        :param self:
        :type self:
        :param yaml:
        :type yaml: str or dictionary
        :param json_schema:
        :type json_schema:
        :param application:
        :type application:
        """
        self.y = yaml
        self.s = json_schema
        self.a = application

        # if not dictionary
        if not isinstance(self.y, dict) and Path(self.y).resolve().is_file():
            self.config_path = Path(self.y).resolve()
            self.config_data = None

            if self.s is None:
                fre_logger.warning("NO SCHEMA FILE GIVEN, PARSING YAML BY DEFAULT")
                yml_dict = helpers.yaml_load(self.config_path)
                self.schema_url = yml_dict.get(application).get("schema").get("repo")
                self.schema_version = yml_dict.get(application).get("schema").get("version")
                self.schema_file = yml_dict.get(application).get("schema").get("file")
        else:
            self.config_path = None
            self.config_data = self.y

            if self.s is None:
                fre_logger.warning("NO SCHEMA FILE GIVEN, PARSING YAML BY DEFAULT")
                self.schema_url = self.y.get(application).get("schema").get("repo")
                self.schema_version = self.y.get(application).get("schema").get("version")
                self.schema_file = self.y.get(application).get("schema").get("file")

    def validate(self):
        """
        """
        use_uwtools_logger()
        if self.s is None:
            with TemporaryDirectory(prefix = "fre-schema-") as tmp_dir:
                schema = subprocess.run( ['git', 'clone', f'--branch={self.schema_version}', self.schema_url,
                                           f'{tmp_dir}/gfdl_msd_schema'], capture_output = True,
                                           text = True, check = True)
                uhm = f" {self.schema_url}, file: {self.schema_file}"
                result = config.validate(schema_file = Path(f'{tmp_dir}/gfdl_msd_schema/FRE/{self.schema_file}'),
                                         config_data = self.config_data,
                                         config_path = self.config_path,
                                         stdin_ok=False)
        else:
            uhm = Path(self.s).resolve()
            result = config.validate(schema_file = uhm,
                                     config_data = self.config_data,
                                     config_path = self.config_path,
                                     stdin_ok=False)

####raise will onyl look nice if the yaml is a file, NOT a dict
        if not result:
            fre_logger.error("")
            fre_logger.error("*** ERR: YAML CONFIG NOT VALID AGAINST SCHEMA ***")
            fre_logger.error(f"     - YAML CONFIG: {self.config_path}")
            fre_logger.error(f"     - SCHEMA: {uhm}")
            raise ValueError(f"*** FIX YAML CONFIGURATION TO CONTINUE ***")

def validate_subtool(yaml: Union[str, dict], json_schema: str, application: str):
    """
    Validate the YAML file against the json schema. 

    :param yaml: is the YAML file to validate
    :type yaml: string or dictionary
    :param json_schema: is the json schema to validate the YAML against
    :type json_schema: string
    """
    # initiliaze object 
    init_obj = ValidateYaml(yaml, json_schema, application)

    # validate the yaml against the json schema
    validate_rtype = init_obj.validate()
