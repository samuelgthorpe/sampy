#!/usr/bin/env python
"""
Initialize codex persisted context workflow from template

# NOTES
# ----------------------------------------------------------------------------|


Written May 06, 2026
By Samuel Thorpe
"""


# # Imports
# -----------------------------------------------------|
import argparse
import os
import shutil


# # Defs
# -----------------------------------------------------|
def main(proj_dir):
    """Run main method."""
    user = os.environ.get('USER')
    codex_template = f'/home/{user}/Templates/codex-context'
    codex_root = os.path.join(proj_dir, '.codex-context')
    if os.path.exists(codex_root) is False:
        shutil.copytree(codex_template, codex_root)
        print('.codex-context initialized.')
    else:
        print('codex-context already exists. Skipping.')


# # Main Entry
# -----------------------------------------------------|
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-project_dir',
        type=str,
        help='path to project in which to initialize codex',
        default=".")
    args = parser.parse_args()
    exp = main(args.project_dir)
