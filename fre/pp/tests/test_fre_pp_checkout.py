#!/usr/bin/env python3

from fre import pp
from fre.pp import checkoutScript

import os

#from click.testing import CliRunner
#runner = CliRunner()

#tests are structured in the manner of: 
#https://click.palletsprojects.com/en/8.1.x/testing/
#general intent for these tests is that each fre tool has 2 commandline tests:
#help, command does not exist

#Test list: 
#-- fre pp checkout
#--- does it check out a branch not  named "main"

######### setup

#-- fre pp checkout
def test_cli_fre_pp_checkout_main():
    checkout_dir = os.path.expanduser("~/cylc-src")
    experiment = "fake1"
    platform = "forgery1"
    target = "artifice1"
    checkoutstat = pp.checkoutScript._checkoutTemplate(experiment, platform, target, 
                                                git_checkout_dir = checkout_dir)
    branch_checkout = pp.checkoutScript.git_report_branch(checkout_dir)
    print(os.listdir(checkout_dir))
    assert branch_checkout == "main"
    
def test_cli_fre_pp_checkout_testbranch():
    checkout_dir = os.path.expanduser("~/cylc-src")
    experiment = "fake2"
    platform = "forgery2"
    target = "artifice2"
    branch = "testbranch"
    checkoutstat = fre.pp.checkoutScript._checkoutTemplate(experiment, platform, target, 
                                                branch=branch,
                                                git_checkout_dir = checkout_dir)
    branch_checkout = fre.pp.checkoutScript.git_report_branch(checkout_dir)
    print(os.listdir(checkout_dir))
    assert branch_checkout == branch
    
############ cleanup
