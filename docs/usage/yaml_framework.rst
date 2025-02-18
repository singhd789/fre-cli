In order to utilize these FRE tools, a distrubuted YAML structure is required. This framework includes

  - model yaml
  - compile yaml
  - platforms yaml
  - post-processing yamls
  - analysis yamls

Throughout the compilation and post-processing steps, combined yamls that will be parsed for information are created. Yamls follow a dictionary-like structure with [key]: [value] fields.

YAML Formatting
----------
.. include:: usage/yaml_dev/yaml_formatting.rst

Model Yaml
----------
.. include:: usage/yaml_dev/model_yaml.rst

Compile Yaml
----------
The compile yaml defines compilation information including component names, repos, branches, necessary flags, and necessary overrides. This is discussed more in the "Build FMS Model" section.

Platforms Yaml
----------
.. include:: usage/yaml_dev/platforms_yaml.rst

Post-processing Yaml
----------
The post-processing yamls include information specific to experiments, such as directories to data and other scripts used, switches, and component information. The post-processing yaml can further define more fre_properties that may be experiment specific. If there are any repeated reusable variables, the ones set in this yaml will overwrite those set in the model yaml. This is discussed further in the “Postprocess FMS History Output” section.

#.. include:: usage/yaml_dev/pp_yaml.rst

:ref:`history-files`

Analysis Yaml
----------
.. include:: usage/yaml_dev/analysis_yaml.rst
