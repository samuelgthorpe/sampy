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
import subprocess


# # Globals
# -----------------------------------------------------|
IGNORE_PATHS = set(['/home/sam/Documents/Codex'])
default_backup_dir = (
    "/mnt/c/Users/SamThorpe/"
    "OneDrive - NeuraSignal Inc/"
    "Documents/Codex/context-backups"
)


# # Defs
# -----------------------------------------------------|
def main(args):
    """Run main method."""
    os.makedirs(args.backup_dir, exist_ok=True)
    for root, dirs, files in os.walk(os.path.expanduser("~")):
        if ".codex-context" in dirs and not _check_ignore(root):
            src = os.path.join(root, ".codex-context")
            rel_pth = os.path.relpath(src, os.path.expanduser("~"))
            dst = os.path.join(args.backup_dir, rel_pth)

            os.makedirs(dst, exist_ok=True)
            try:
                subprocess.run(
                    ["rsync", "-avh", f"{src}/", f"{dst}/"],
                    check=True,
                )
            except subprocess.CalledProcessError as exc:
                print(
                    f"Backup failed for {src}: "
                    f"rsync exited with code {exc.returncode}"
                )
            else:
                print(f"Backed up {src} to {dst}")


def _check_ignore(path):
    """Check if the given path should be ignored."""
    if path.startswith(default_backup_dir):
        return True
    for ignore_path in IGNORE_PATHS:
        if path.startswith(ignore_path):
            return True

    return False


# # Main Entry
# -----------------------------------------------------|
if __name__ == "__main__":
    args = argparse.ArgumentParser(
        description="Backup .codex-context directories across projects.")
    args.add_argument(
        "--backup-dir",
        type=str,
        default=default_backup_dir,
        help="Directory to store the backups.")
    args = args.parse_args()
    main(args)
