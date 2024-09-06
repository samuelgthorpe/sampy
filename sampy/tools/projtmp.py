#! /usr/bin/python3
"""
Project template generator.

# NOTES
# ----------------------------------------------------------------------------|


Written June 19, 2024
By Samuel Thorpe
"""


# # Imports
# -----------------------------------------------------|
import os
from os.path import basename, join
import argparse
import shutil
import subprocess
import json
import requests
from git import Repo


# # Globals
# -----------------------------------------------------|
DEFAULT_PROJECT_DIR = '/home/sam/Projects'
DEFAULT_LOCAL_TEMPLATE = '/home/sam/Repos/st-experiment-template'
REMOTE_URL = 'git@github.com:samuelgthorpe'


# # Defs
# -----------------------------------------------------|
def main(args):
    """Run main method."""
    proj_dir = join(args.project_dir, args.project_name)
    repo_dir = join(proj_dir, args.project_name)

    init_project_dir(proj_dir, repo_dir, args.project_name, sync=args.sync)
    update_template(repo_dir, args.project_name)
    init_repo(args.project_name, repo_dir, sync=args.sync)
    init_venv(proj_dir, args.project_name)


def init_project_dir(proj_dir, repo_dir, proj_name, sync=False):
    """Initiate project directory.

    Args:
        proj_dir (str, path): Path to save project
        repo_dir (str, path): Path to repo within project
        proj_name (str): Project name (use hyphens as sep!)
        sync (bool, optional): if True then pull template from github and sync
                               new project repo to github as well.
    """
    os.makedirs(proj_dir)
    if sync:
        _pull_template(proj_dir, repo_dir, proj_name)
    else:
        shutil.copytree(DEFAULT_LOCAL_TEMPLATE, repo_dir)

    # delete template .git directory
    template_git_dir = join(repo_dir, '.git')
    shutil.rmtree(template_git_dir)


def _pull_template(proj_dir, repo_dir, proj_name):
    """Pull template from github."""
    os.makedirs(repo_dir)
    template_url = f'{REMOTE_URL}/st-experiment-template.git'
    Repo.clone_from(template_url, repo_dir, branch='main')


def update_template(repo_dir, project_name):
    """Update template.

    Replaces all occurences of template name with project name.
    Same for references to snake_case template src module.

    Args:
        repo_dir (str, path): Path to repo within project
        proj_name (str): Project name (use hyphens as sep!)
    """
    template_name = basename(DEFAULT_LOCAL_TEMPLATE)
    template_src_dir = template_name.replace('-', '_')
    template_src_pth = join(repo_dir, template_src_dir)
    src_dir = project_name.replace('-', '_')
    src_pth = join(repo_dir, src_dir)
    os.rename(template_src_pth, src_pth)

    # replace all occurences of template strings in repo
    zipd = [(template_src_dir, src_dir), (template_name, project_name)]
    for to_replace, replace_with in zipd:
        term = subprocess.Popen(
            ["find", repo_dir, "-type", "f"],
            stdout=subprocess.PIPE
            )
        find_out = term.communicate()[0]
        term2 = subprocess.Popen(
            ["xargs", "sed", "-i", f"s/{to_replace}/{replace_with}/g"],
            stdin=subprocess.PIPE)
        term2.communicate(find_out)  # noqa: F841


def init_repo(project_name, repo_dir, sync=False):
    """Init git repository.

    Args:
        proj_name (str): Project name (use hyphens as sep!)
        repo_dir (str, path): Path to repo within project
        sync (bool, optional): if True then pull template from github and sync
                               new project repo to github as well.
    """
    repo = Repo.init(repo_dir)
    repo.git.add(all=True)
    repo.git.commit('-m', 'init project template')

    # if specified, create new github repo and sync
    if args.sync:
        init_github_repo(project_name)
        repo_url = f'{REMOTE_URL}/{project_name}.git'
        remote = repo.create_remote('origin', url=repo_url)
        remote.push(refspec='main:main')


def init_github_repo(project_name):
    """Init repo on Github.

    Args:
        proj_name (str): Project name (use hyphens as sep!)

    Returns:
        req (request object): result of github API call

    Raises:
        Exception: Description
    """
    request_url = 'https://api.github.com/user/repos'
    payload = {
        "name": project_name,
        "homepage": "https://github.com",
        "private": True,
        "has_issues": True,
        "has_wiki": True
        }

    req = requests.post(
        request_url,
        auth=('samuelgthorpe', os.environ["GITHUB_API_TOKEN"]),
        data=json.dumps(payload))

    if req.status_code != 201:
        print(req)
        raise Exception('Something went wrong')

    return req


def init_venv(proj_dir, proj_name):
    """Init virtual environment.

    Args:
        proj_dir (str, path): Path to save project
        proj_name (str): Project name (use hyphens as sep!)
    """
    venv_name = f'.venv-{proj_name}'
    current = os.getcwd()
    os.chdir(proj_dir)

    # create venv and upgrade pip
    subprocess.call(['python3', '-m', 'venv', venv_name])
    subprocess.call([
        f'{proj_dir}/{venv_name}/bin/pip',
        'install', '--upgrade', 'pip'])

    os.chdir(current)


# # Main Entry
# -----------------------------------------------------|
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'project_name',
        type=str,
        help='project name (use hyphens as sep)')
    parser.add_argument(
        '-project_dir',
        type=str,
        help='project directory',
        default=DEFAULT_PROJECT_DIR)
    parser.add_argument(
        '--sync',
        action="store_true",
        help='use github template and push new project')
    args = parser.parse_args()
    main(args)
