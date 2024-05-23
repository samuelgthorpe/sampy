"""
System tests to probe the container environment.

Note these can also be done manually with the make docker.test.shell command
to launch an interactive terminal into the container and probe the
dependencies/connections


# NOTES
# ----------------------------------------------------------------------------|


written March 2024
by Samuel Thorpe
"""


# # Imports
# -----------------------------------------------------|
import argparse
import numpy as np
import scipy as sp
import pandas as pd
import boto3


# # Defs
# -----------------------------------------------------|
def main(local=False):
    """Run basic checks for built container."""
    print(f'\nCHECKING LIBS\n{"-"*40}>>>')
    for mod in [np, sp, pd, boto3]:
        print(f"{mod.__name__} version: {mod.__version__}")


# # Main Entry
# -----------------------------------------------------|
if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description='test environment')
    PARSER.add_argument("--local", action="store_true")
    ARGS = PARSER.parse_args()
    main(ARGS.local)
