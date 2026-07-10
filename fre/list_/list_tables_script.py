## combine into dictionary --> if combining ALL, combining could be put into fre/list/__init__.py
## validate dictionary
## list relevant areas
import logging
from fre.yamltools.helpers import yaml_load

fre_logger = logging.getLogger(__name__)

def parse_for_tables(dataset_info, val):
    """
    """
    tables_list = []

    for dataset_value in dataset_info.values():
        for i in dataset_value:
#        ##whats the difference between table and yaml label in inputs???##

            if isinstance(val, str):
                if i.get("label") == val:
                    tables_list.append(i.get('source'))
            elif isinstance(val, list):
                for v in val:
                    if i.get("label") == v:
                        tables_list.append(i.get('source'))

    return tables_list

def list_tables_subtool(yamlfile, diag_tables, data_tables, field_tables, all_tables):
    """
    """
    #combine
    yml = yaml_load(yamlfile)

    #validate

    #parse
    target_table = "all"
    if diag_tables:
        target_table = "diagYaml"
    elif data_tables:
        target_table = "dataYaml"
    elif field_tables:
        target_table = "fieldYaml"
    elif all_tables:
        target_table = ["diagYaml", "dataYaml","fieldYaml"]

    ##### figure out --> where are tables usually listed #####
    ##### whats beneficial --> listing all tables associated with a exp names in input, listing tables referenced/associated with click passed experiment? #####

    dataset_info = yml["run"]["input"]["datasets"]

    tl = parse_for_tables(dataset_info, val = target_table)

    # set logger level to INFO
    former_log_level = fre_logger.level
    fre_logger.setLevel(logging.INFO)

    fre_logger.info("Tables:")
    for t in tl:
        fre_logger.info("  - %s", t)

    fre_logger.setLevel(former_log_level)

    return tl
