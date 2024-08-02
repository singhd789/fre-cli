#!/usr/bin/env python3

from fre import fre
from fre import frepp
from frepp import checkoutScript

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
    
    result = runner.invoke(fre.fre, args=['--help', "pp checkout"])
    assert result.exit_code == 0
    
def test_cli_fre_pp_checkout_testbranch():
    result = runner.invoke(fre.fre, args=['optionDNE', "pp checkout"])
    assert result.exit_code == 2
    
############ cleanup
