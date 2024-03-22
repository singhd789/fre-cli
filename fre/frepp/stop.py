#!/usr/bin/env python

import os
import subprocess
import click

@click.command()

def stop_workflow(experiment, platform, target):
    """
    Stop and clean up after the workflow identified by
    the combination of experiment, platform and target
    """

    name = experiment + '__' + platform + '__' + target
    stop_cmd  = f"cylc stop {name}"
    clean_cmd = f"cylc clean {name}"
    subprocess.run(stop_cmd, shell=True, check=True)
    subprocess.run(clean_cmd, shell=True, check=True)
