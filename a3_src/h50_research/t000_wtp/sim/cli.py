# -*- coding: utf-8 -*-
"""
Simulation system command line interface logic.

"""


import logging
import os
import sys
import tempfile

import click

import sim.sim

# -----------------------------------------------------------------------------
@click.group(name = 'sim')
def main():
    """
    Simulation system prototype.

    """
    pass


# -----------------------------------------------------------------------------
@main.command()
@click.pass_context
def run(ctx):
    """
    Run simulation.

    """
    sim.sim.main()
    return 0
