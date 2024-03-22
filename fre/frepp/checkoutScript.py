#!/usr/bin/env python

# Author: Bennett Chang
# Description: 

import os
from pathlib import Path
import subprocess
from subprocess import PIPE, STDOUT
import click
import re

#############################################

package_dir = os.path.dirname(os.path.abspath(__file__))

#############################################

@click.command()
@click.option("-e",
              "--experiment", 
              type=str, 
              help="Experiment name", 
              required=True)
@click.option("-p", 
              "--platform",
              type=str, 
              help="Platform name", 
              required=True)
@click.option("-t",
              "--target", 
              type=str, 
              help="Target name", 
              required=True)
def checkoutTemplate(experiment, platform, target):
    """
    Checkout the template file
    """
    # Create the directory if it doesn't exist
    directory = os.path.expanduser("~/cylc-src")
    os.makedirs(directory, exist_ok=True)

    # Change the current working directory
    os.chdir(directory)

    # Set the name of the directory
    name = f"{experiment}__{platform}__{target}"

    # Clone the repository with depth=1
    click.echo("cloning into directory " + directory + "/" + name)
    print("this is my local copy")
    preexist_error = f"fatal: destination path '{name}' already exists and is not an empty directory."
    clonecmd = f"git clone --depth=1 --recursive https://gitlab.gfdl.noaa.gov/fre2/workflows/postprocessing.git {name}"
    cloneproc = subprocess.run(clonecmd, shell=True, check=False, stdout=PIPE, stderr=STDOUT)
    if not cloneproc.returncode == 0:
        if re.search(preexist_error.encode('ASCII'),cloneproc.stdout) is not None:
            argstring = f" -e {experiment} -p {platform} -t {target}"
            stop_report = "\n".join([f"Error in checkoutTemplate: the workflow definition specified by -e/-p/-t already exists at the location ~/cylc-src/{name}",
            #"To run this experiment, either change the experiment name in the configutation file",
            #f"> cat $configuration_file | grep {name}",
            #f"> echo $config_file | sed -e 's:{name}:$new-experiment-name:g' > $new_config_file",
            "To run this experiment clean up the previous experiment of this name by running",
            "> fre pp stop " + argstring])
            click.echo(stop_report)
            return 1
        else:
            print(cloneproc.stdout)
            return 1

#############################################

if __name__ == '__main__':
    checkoutTemplate()
