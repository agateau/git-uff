#!/usr/bin/env python3
# Copyright 2021 Aurélien Gâteau <mail@agateau.com>
# SPDX-License-Identifier: Apache-2.0
"""
Prints the forge url for a given file or path of a Git repository checkout.
"""
import argparse
import sys

from pathlib import Path

from git import Repo

from git_uff import converters
from git_uff.converters import Converter


class ToolError(Exception):
    pass


CONVERTERS = []


def add_converter(converter_name, url):
    converter_class = getattr(converters, f"{converter_name}Converter")
    converter = converter_class(url)
    CONVERTERS.append(converter)


def load_config():
    add_converter("GitHub", "github.com")
    add_converter("GitLab", "invent.kde.org")
    add_converter("SourceHut", "git.sr.ht")
    add_converter("CGit", "git.zx2c4.com")


def get_repo_root(path: Path) -> Path:
    original = path
    while not (path / ".git").exists():
        if len(path.parts) == 1:
            raise ToolError(f"{original} is not in a git repository")
        path = path.parent
    return path


def find_converter(repo) -> (Converter, str):
    for remote in repo.remotes:
        for url in remote.urls:
            for converter in CONVERTERS:
                if converter.match(url):
                    return converter, url
    raise ToolError("Don't know how to get an url for this repository")


def main():
    parser = argparse.ArgumentParser()
    parser.description = __doc__

    parser.add_argument("path", help="File for which we want the url")
    parser.add_argument("-l", "--line", type=int, help="Line to point to")

    args = parser.parse_args()

    load_config()

    try:
        path = Path(args.path).resolve(strict=True)
    except FileNotFoundError:
        print(f"{path} does not exist")
        return 1

    try:
        repo_root = get_repo_root(path)
        repo = Repo(repo_root)
        converter, remote_url = find_converter(repo)
        url = converter.run(remote_url, repo.active_branch.name,
                            path.relative_to(repo_root), args.line)

        print(url)
    except ToolError as e:
        print(e)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
