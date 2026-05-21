#!/usr/bin/env python
"""
Tool to backup .codex-context directories across projects.

The tool should scan the home directory for .codex-context directories, and
sync them to a designated backup location.

# NOTES
# ----------------------------------------------------------------------------|


Written May 21, 2026
By Samuel Thorpe
"""


# # Imports
# -----------------------------------------------------|
import os
import argparse


# # Defs
# -----------------------------------------------------|
def main(args):
    """Run main method."""
    os.makedirs(args.backup_dir, exist_ok=True)
    for root, dirs, files in os.walk(os.path.expanduser("~")):
        if ".codex-context" in dirs and not root.startswith(args.backup_dir):
            src = os.path.join(root, ".codex-context")
            rel_pth = os.path.relpath(src, os.path.expanduser("~"))
            dst = os.path.join(args.backup_dir, rel_pth)
            os.makedirs(dst, exist_ok=True)
            os.system(f"rsync -avh {src}/ {dst}/")
            print(f"Backed up {src} to {dst}")


# # Main Entry
# -----------------------------------------------------|
if __name__ == "__main__":
    args = argparse.ArgumentParser(
        description="Backup .codex-context directories across projects.")
    args.add_argument(
        "--backup-dir",
        type=str,
        default=os.path.expanduser("~/Documents/Codex/context-backups"),
        help="Directory to store the backups.")
    args = args.parse_args()
    main(args)
