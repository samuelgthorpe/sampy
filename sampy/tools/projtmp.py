#!/usr/bin/env python3
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
from pathlib import Path
import shutil
import subprocess
import json
import requests
from git import Repo


# # Globals
# -----------------------------------------------------|
DEFAULT_PROJECT_DIR = join(Path.home(), 'Projects')
DEFAULT_LOCAL_TEMPLATE = join(Path.home(), 'Repos', 'st-experiment-template')
REMOTE_URL = 'git@github.com:samuelgthorpe'


# # Defs
# -----------------------------------------------------|
def main(args):
    """Run main method."""
    proj_dir = join(args.project_dir, args.project_name)
    repo_dir = join(proj_dir, args.project_name)

    init_project_dir(proj_dir, repo_dir, args)
    update_template(repo_dir, args.project_name)
    init_repo(repo_dir, args)
    init_venv(proj_dir, args.project_name)


def init_project_dir(proj_dir, repo_dir, args):
    """Initiate project directory.

    Args:
        proj_dir (str, path): Path to save project
        repo_dir (str, path): Path to repo within project
        args.project_name (str): project name
        args.sync (bool, optional): 
            if True then pull template from github and sync new project repo 
            to github as well.
        args.github_user (str): github username (if args.sync is True)
        args.github_api_token (str): github api token (if args.sync is True)
    """
    os.makedirs(proj_dir)
    if args.sync:
        _pull_template(proj_dir, repo_dir, args.project_name)
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
        project_name (str): Project name (use hyphens as sep!)
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


def init_repo(repo_dir, args):
    """Init git repository.

    Args:
        proj_name (str): Project name (use hyphens as sep!)
        repo_dir (str, path): Path to repo within project
        args.project_name (str): project name
        args.sync (bool, optional): 
            if True then pull template from github and sync new project repo to 
            github as well.
        args.github_user (str): github username (if args.sync is True)
        args.github_api_token (str): github api token (if args.sync is True)
    """
    repo = Repo.init(repo_dir)
    repo.git.add(all=True)
    repo.git.commit('-m', 'init project template')

    # if specified, create new github repo and sync
    if args.sync:
        init_github_repo(args.project_name, args.github_user, 
                         args.github_api_token)
        repo_url = f'{REMOTE_URL}/{args.project_name}.git'
        remote = repo.create_remote('origin', url=repo_url)
        remote.push(refspec='main:main')


def init_github_repo(project_name, github_user, github_api_token):
    """Init repo on Github.

    Args:
        proj_name (str): Project name (use hyphens as sep!)
        github_user (str): github username
        github_api_token (str): github api token

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
        auth=(github_user, github_api_token),
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
    current = os.getcwd()
    os.chdir(join(proj_dir, proj_name))

    # create venv and upgrade pip
    subprocess.call(['python', '-m', 'venv', '.venv'])
    subprocess.call([
        join(proj_dir, proj_name, '.venv', 'bin', 'pip'),
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
    parser.add_argument(
        '-github_api_token',
        type=str,
        help='github_api_token',
        default=os.environ.get("GITHUB_API_TOKEN"))
    parser.add_argument(
        '-github_user',
        type=str,
        help='github_user',
        default=os.environ.get("GITHUB_USER"))
    args = parser.parse_args()
    main(args)
