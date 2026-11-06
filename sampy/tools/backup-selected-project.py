#!/usr/bin/env python3
"""Copy a whole project into a dated snapshot suitable for OneDrive syncing.

Includes hidden files and preserves symbolic links without following them outside
of the project. Link targets outside the project are therefore not backed up.
A completed local copy still requires OneDrive to finish syncing on Windows.
"""

import argparse
from datetime import datetime
from pathlib import Path
import shutil
import sys
import tempfile


DEFAULT_BACKUP_DIR = Path(
    '/mnt/c/Users/SamThorpe/OneDrive - NeuraSignal Inc/Documents/SelectedBackup'
)


def backup_project(project_dir, backup_dir):
    """Return a completed snapshot path; retain partial copies visibly on failure."""
    source = Path(project_dir).expanduser().resolve(strict=True)
    destination = Path(backup_dir).expanduser().resolve()
    if not source.is_dir():
        raise ValueError(f'Project is not a directory: {source}')
    if source == destination or source in destination.parents:
        raise ValueError('Backup directory must be outside the project directory.')
    if not source.name:
        raise ValueError('Choose a project directory rather than the filesystem root.')

    # Resolve the project-specific folder too, so an existing symlink cannot
    # redirect the copy back into the source and recursively copy the backup.
    project_backups = (destination / source.name).resolve()
    if project_backups == source or source in project_backups.parents:
        raise ValueError('Project backup folder resolves inside the source project.')
    project_backups.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().astimezone().strftime('%Y%m%d-%H%M%S-%f%z')
    snapshot = project_backups / timestamp
    staging = Path(tempfile.mkdtemp(prefix='.incomplete-', dir=project_backups))
    print(f'Copying {source}\n     to {snapshot}', flush=True)
    try:
        # Do not traverse symlinks: external targets and cycles must not expand
        # the requested project scope. copy2 also preserves file timestamps.
        shutil.copytree(source, staging, symlinks=True, dirs_exist_ok=True)
        staging.rename(snapshot)
    except (OSError, shutil.Error) as exc:
        raise RuntimeError(
            f'Backup did not complete. Partial copy retained at {staging}: {exc}'
        ) from exc
    return snapshot


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'project_dir', nargs='?', default='.', type=Path,
        help='Project to copy (default: current directory).',
    )
    parser.add_argument(
        '--backup-dir', '--destination', '-d', default=DEFAULT_BACKUP_DIR,
        type=Path, help=f'Backup root (default: {DEFAULT_BACKUP_DIR}).',
    )
    args = parser.parse_args(argv)
    try:
        snapshot = backup_project(args.project_dir, args.backup_dir)
    except (OSError, ValueError, RuntimeError, shutil.Error) as exc:
        print(f'Backup failed: {exc}', file=sys.stderr)
        return 1
    print(f'Backup complete: {snapshot}\nCheck OneDrive on Windows for sync completion.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
