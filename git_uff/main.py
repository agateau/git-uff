#!/usr/bin/env python3
# Copyright 2021 Aurélien Gâteau <mail@agateau.com>
# SPDX-License-Identifier: Apache-2.0
"""
Prints the forge URL for a given file or path of a Git repository checkout.
"""
import argparse
import sys

from pathlib import Path
from typing import Tuple, List

from git import Repo

from git_uff.config import load_config
from git_uff.converters import Converter, get_converter_classes_dict


EPILOG = """
New forges can be declared in git configuration. You can do so using
`git config`, like this:

    git config --global uff.<forge_base_url>.forge <forge>

Where <forge> must be one of: {converter_list}.

For example to declare that example.com uses GitLab:

    git config --global uff.example.com.forge gitlab
"""


class ToolError(Exception):
    pass


def get_repo_root(path: Path) -> Path:
    original = path
    while not (path / ".git").exists():
        if len(path.parts) == 1:
            raise ToolError(f"{original} is not in a git repository")
        path = path.parent
    return path


def find_converter(converters: List[Converter], repo: Repo) -> Tuple[Converter, str]:
    """Look for a converter matching one of the remotes of repo, returns a
    tuple of the converter and the URL for the matching remote."""
    for remote in repo.remotes:
        for url in remote.urls:
            for converter in converters:
                if converter.match(url):
                    return converter, url
    raise ToolError("Don't know how to get an URL for this repository."
                    " Run `git uff --help` to learn how to fix this.")


def get_epilog() -> str:
    converter_names = get_converter_classes_dict()
    converter_list = ", ".join(sorted(converter_names))
    return EPILOG.format(converter_list=converter_list)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog=get_epilog(),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("path", help="File for which we want the URL")
    parser.add_argument("-b", "--branch",
                        help="Use branch BRANCH instead of the current one",
                        metavar="BRANCH")
    parser.add_argument("-p", "--permalink", action="store_true",
                        help="Replace the branch in the URL with the commit"
                        " it points to")
    parser.add_argument("-l", "--line", type=int, help="Line to point to")

    args = parser.parse_args()

    try:
        path = Path(args.path).resolve(strict=True)
    except FileNotFoundError:
        print(f"File '{args.path}' does not exist")
        sys.exit(1)

    try:
        repo_root = get_repo_root(path)
        repo = Repo(repo_root)
        converters = load_config(repo)
        converter, remote_url = find_converter(converters, repo)
        if args.branch:
            branch = args.branch
        else:
            branch = repo.active_branch.name
        if args.permalink:
            branch = repo.rev_parse(branch).hexsha
        url = converter.run(remote_url, branch,
                            path.relative_to(repo_root), args.line)

        print(url)
    except ToolError as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
