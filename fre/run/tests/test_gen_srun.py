"""
Test fre run gen-srun
"""
from pathlib import Path
import pytest
from fre.run import generate_srun_script
import logging

@pytest.fixture
def test_yaml():
    """
    """
    layouts = {"layouts": {"layout1": {"job_wallclock": "16:00:00",
                                       "atm": {"ranks": "576", "threads": 2, "layout": "4,24", "io_layout": "1,4", "mask_table": None},
                                       "lnd": {"ranks": None, "threads": None, "layout": "4,24", "io_layout": "1,4", "mask_table": None},
                                       "ocn": {"ranks": "0", "threads": None, "layout": "96,6", "io_layout": "1,3", "mask_table": None},
                                       "ice": {"ranks": None, "threads": None, "layout": "96,6", "io_layout": "1,3", "mask_table": None}},
                           "layout2": {"job_wallclock": "16:00:00",
                                       "atm": {"ranks": "4608", "threads": 4, "layout": "24,32", "io_layout": "1,4", "mask_table": None},
                                       "lnd": {"ranks": None, "threads": None, "layout": "24,32", "io_layout": "1,4", "mask_table": None},
                                       "ocn": {"ranks": "0", "threads": None, "layout": "128,36", "io_layout": "1,4", "mask_table": None},
                                       "ice": {"ranks": None, "threads": None, "layout": "128,36", "io_layout": "1,4", "mask_table": None}},
                           "coupled_layout": {"job_wallclock": "16:00:00",
                                              "atm": {"ranks": "576", "threads": 2, "layout": "4,24", "io_layout": "1,4", "mask_table": None},
                                              "lnd": {"ranks": None, "threads": None, "layout": "4,24", "io_layout": "1,4", "mask_table": None},
                                              "ocn": {"ranks": "2021", "threads": 1, "layout": "64,42", "io_layout": "1,3", "mask_table": None},
                                              "ice": {"ranks": None, "threads": None, "layout": "96,6", "io_layout": "1,3", "mask_table": None}},
                          }
              }

    return layouts

def test_gen_srun_subtool(test_yaml, caplog):
    """
    No submit
    """
    yml = test_yaml
    experiment = ("layout1",)

    caplog.set_level(logging.INFO)
    result = generate_srun_script.gen_srun_subtool(yamlfile = yml,
                                                   experiment = experiment,
                                                   submit = False)

    expected_out = f"For {experiment[0]}: srun --ntasks=576 --cpus-per-task=2 --export=ALL,OMP_NUM_THREADS=2 [executable/path]"
    assert expected_out in caplog.text

def test_multiple_srun_cmds(test_yaml, caplog):
    """
    """
    yml = test_yaml
    experiment = ("layout1", "layout2",)

    caplog.set_level(logging.INFO)
    result = generate_srun_script.gen_srun_subtool(yamlfile = yml,
                                                   experiment = experiment,
                                                   submit = False)

    expected_out1 = f"For {experiment[0]}: srun --ntasks=576 --cpus-per-task=2 --export=ALL,OMP_NUM_THREADS=2 [executable/path]"
    expected_out2 = f"For {experiment[1]}: srun --ntasks=4608 --cpus-per-task=4 --export=ALL,OMP_NUM_THREADS=4 [executable/path]"
    assert "*** More than one experiment passed ***" in caplog.text
    assert expected_out1 in caplog.text
    assert expected_out2 in caplog.text

def test_srun_for_coupled_exp(test_yaml, caplog):
    """
    """
    yml = test_yaml
    experiment = ("coupled_layout",)

    caplog.set_level(logging.INFO)
    result = generate_srun_script.gen_srun_subtool(yamlfile = yml,
                                                   experiment = experiment,
                                                   submit = False)

    expected_out = f"For {experiment[0]}: srun --ntasks=576 --cpus-per-task=2 --export=ALL,OMP_NUM_THREADS=2 [executable/path] : --ntasks=2021 --cpus-per-task=1 --export=ALL,OMP_NUM_THREADS=1 [executable/path]"
    assert expected_out in caplog.text

#def test_load_yaml():
#    """
#    """
#    yml = 
#    experiment = ("layout1",)
#    
#    init = generate_srun_script.GenSRUN(yamlfile=yml, 
#                                        experiment=experiment,
#                                        submit=False)
#    result = init.load_yaml()
#
#    assert expected_cmd == output
#

def test_get_layout_info(test_yaml):
    """
    """
    #yml =
    experiment = ("layout1",)
    init = generate_srun_script.GenSRUN(yamlfile = "dummy.yaml",
                                        experiment = experiment,
                                        submit = False)
    result = init.get_layout_info(test_yaml)

    expected_layout = [{"layout1": {"job_wallclock": "16:00:00",
                                   "atm": {"ranks": "576", "threads": 2, "layout": "4,24", "io_layout": "1,4", "mask_table": None},
                                   "lnd": {"ranks": None, "threads": None, "layout": "4,24", "io_layout": "1,4", "mask_table": None},
                                   "ocn": {"ranks": "0", "threads": None, "layout": "96,6", "io_layout": "1,3", "mask_table": None},
                                   "ice": {"ranks": None, "threads": None, "layout": "96,6", "io_layout": "1,3", "mask_table": None}
                                  }
                       }]
    assert result == expected_layout

def test_exp_not_in_layout(test_yaml):
    """
    """
    yml = test_yaml
    experiment = ("exp_no_layout",)

    with pytest.raises(ValueError, match="Experiment not defined in the layouts.yaml!!"):
        generate_srun_script.gen_srun_subtool(yamlfile = yml,
                                              experiment = experiment,
                                              submit = False)


def test_compose_srun():
    """
    """
    #yml =
    experiment = ("layout1",)
    layout_list = [{"layout1": {"job_wallclock": "16:00:00",
                                "atm": {"ranks": "576", "threads": 2, "layout": "4,24", "io_layout": "1,4", "mask_table": None},
                                "lnd": {"ranks": None, "threads": None, "layout": "4,24", "io_layout": "1,4", "mask_table": None},
                                "ocn": {"ranks": "0", "threads": None, "layout": "96,6", "io_layout": "1,3", "mask_table": None},
                                "ice": {"ranks": None, "threads": None, "layout": "96,6", "io_layout": "1,3", "mask_table": None}
                               }
                   }]
    init = generate_srun_script.GenSRUN(yamlfile = "dummy.yaml",
                                        experiment = experiment,
                                        submit = False)
    result = init.compose_srun(layout_list)

    expected_cmd = "srun --ntasks=576 --cpus-per-task=2 --export=ALL,OMP_NUM_THREADS=2 [executable/path]"

    assert result[0] == expected_cmd
