#!/usr/bin/env python

# Author: Bennett Chang
# Description:

import os
import sys
from pathlib import Path
import subprocess
from subprocess import PIPE
from subprocess import STDOUT
import click
import re

#############################################

def _checkoutTemplate(experiment, platform, target, branch='main', 
                      git_checkout_dir = os.path.expanduser("~/cylc-src")):
    """
    Checkout the workflow template files from the repo
    """
    # Create the directory if it doesn't exist
    os.makedirs(git_checkout_dir, exist_ok=True)

    # Set the name of the directory
    name = f"{experiment}__{platform}__{target}"

    # Clone the repository with depth=1; check for errors
    click.echo("cloning experiment into directory " + directory + "/" + name)
    clonecmd = (
        f"git clone -b {branch} --single-branch --depth=1 --recursive "
        f"-C {git_checkout_dir} "
        f"https://github.com/NOAA-GFDL/fre-workflows.git {name}" )
    preexist_error = f"fatal: destination path '{name}' exists and is not an empty directory."
    click.echo(clonecmd)
    cloneproc = subprocess.run(clonecmd, shell=True, check=False, stdout=PIPE, stderr=STDOUT)
    if not cloneproc.returncode == 0:
        if re.search(preexist_error.encode('ASCII'),cloneproc.stdout) is not None:
            argstring = f" -e {experiment} -p {platform} -t {target}"
            stop_report = (
                "Error in checkoutTemplate: the workflow definition specified by -e/-p/-t already"
                f" exists at the location ~/cylc-src/{name}!\n"
                f"In the future, we will confirm that ~/cylc-src/{name} is usable and will check "
                "whether it is up-to-date.\n"
                "But for now, if you wish to proceed, you must delete the workflow definition.\n"
                "To start over, try:\n"
                f"\t cylc stop {name}\n"
                f"\t cylc clean {name}\n"
                f"\t rm -r ~/cylc-src/{name}" )
            sys.exit(stop_report)
            return 1
        else:
            #if not identified, just print the error
            click.echo(clonecmd)
            click.echo(cloneproc.stdout)
        return 1

def git_report_branch(repo):
    '''
    Reports on the name of curent branch; wrapper for system git command
    '''
    gitcmd = f"git rev-parse --abbrev-ref HEAD"
    gitproc = subprocess.run(gitcmd, shell=True, stdout=PIPE, stderr=STDOUT)
    click.echo(gitproc.stdout)
    if not gitproc.returncode == 0:
        sys.exit("Error in git_report_branch: git command exited with status " + 
                 str(gitproc.status) + ". Please query branch from commandline.")
    else:
        return(gitproc.stdout)

#############################################

@click.command()
def checkoutTemplate(experiment, platform, target, branch="main"):
    '''
    Wrapper script for calling checkoutTemplate - allows the decorated version
    of the function to be separate from the undecorated version
    '''
    #For testing, we want to be able to call _checkoutTemplate  without a
    #hard-coded path; for production, we want to enfocrce  a fixed dir struct
    user_checkout_dir = os.path.expanduser("~/cylc-src")
    return _checkoutTemplate(experiment, platform, target, branch, user_checkout_dir)


if __name__ == '__main__':
    checkoutTemplate()
