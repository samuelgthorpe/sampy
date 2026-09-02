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
    codex_template = f'/home/{user}/Templates/codex-workflows'
    template_objs = os.listdir(codex_template)

    # confirm none of the template objects already exist in project directory
    for obj_ in template_objs:
        dst = os.path.join(proj_dir, obj_)
        if os.path.exists(dst):
            print(f'{dst} already exists. Aborting project initialization.')
            return

    # copy template objects to project directory
    for obj_ in template_objs:
        src = os.path.join(codex_template, obj_)
        dst = os.path.join(proj_dir, obj_)
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
    print('.codex-workflow template initialized.')


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
