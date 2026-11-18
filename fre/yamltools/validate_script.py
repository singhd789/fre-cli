"""
"""
import logging
from pathlib import Path
from typing import Union
from uwtools.api import config
from uwtools.api.logging import use_uwtools_logger

fre_logger = logging.getLogger(__name__)

def validate_subtool(yaml: Union[str, dict], json_schema: str):
    """
    Validate the YAML file against the json schema. 

    :param yaml: is the YAML file to validate
    :type yaml: string or dictionary
    :param json_schema: is the json schema to validate the YAML against
    :type json_schema: string
    """
    schema_path = Path(json_schema).resolve()

    use_uwtools_logger()
    if not isinstance(yaml, dict):
        yml_path = Path(yaml).resolve()
        result = config.validate(schema_file = schema_path,
                                 config_data = None,
                                 config_path = yml_path,
                                 stdin_ok=False)

    else:
        result = config.validate(schema_file = schema_path,
                                 config_data = yaml, 
                                 config_path = None,
                                 stdin_ok=False)

    if not result:
        raise ValueError(f"*** ERR: YAML ({yaml}) NOT VALID AGAINST SCHEMA ({schema_path}) ***")
