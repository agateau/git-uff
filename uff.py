#!/usr/bin/env python3
# Copyright 2021 Aurélien Gâteau <mail@agateau.com>
# SPDX-License-Identifier: Apache-2.0
"""
Prints the forge url for a given file or path of a Git repository checkout.
"""
import argparse
import re
import sys

from urllib.parse import quote_plus
from pathlib import Path

from git import Repo


class Converter:
    def match(self, url: str) -> bool:
        return False

    def run(self, repo: Repo, path: Path, line: int = None) -> str:
        return ""


class BasicConverter(Converter):
    # Can contain {base_url}, {project}, {branch}, {escaped_branch}, {path}
    TEMPLATE = ""
    # Can contain {line}
    LINE_SUFFIX = None

    def __init__(self, base_url):
        self.base_url = base_url

    def match(self, url: str) -> bool:
        return self.base_url in url

    def run(self, repo: Repo, remote_url: str, path: Path, line: int = None) -> str:
        dct = {
            "base_url": self.base_url,
            "project": self.get_project(remote_url),
            "branch": repo.active_branch.name,
            "path": path,
            "escaped_branch": quote_plus(repo.active_branch.name),
        }

        url = self.TEMPLATE.format(**dct)
        if line is not None and self.LINE_SUFFIX is not None:
            url += self.LINE_SUFFIX.format(line=line)
        return url

    def get_project(self, remote_url: str) -> str:
        _, project = re.split(re.escape(self.base_url) + "[:/]", remote_url)
        return project.replace(".git", "")


class GitHubLabConverter(BasicConverter):
    TEMPLATE = "https://{base_url}/{project}/blob/{branch}/{path}"
    LINE_SUFFIX = "#L{line}"


class SourceHutConverter(BasicConverter):
    TEMPLATE = "https://{base_url}/{project}/tree/{branch}/{path}"
    LINE_SUFFIX = "#L{line}"


class CGitConverter(BasicConverter):
    TEMPLATE = "https://{base_url}/{project}/tree/{path}?h={escaped_branch}"
    LINE_SUFFIX = "#n{line}"


class ToolError(Exception):
    pass


CONVERTERS = (
    GitHubLabConverter("github.com"),
    GitHubLabConverter("invent.kde.org"),
    SourceHutConverter("git.sr.ht"),
    CGitConverter("git.zx2c4.com"),
)


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

    try:
        path = Path(args.path).resolve(strict=True)
    except FileNotFoundError:
        print(f"{path} does not exist")
        return 1

    try:
        repo_root = get_repo_root(path)
        repo = Repo(repo_root)
        converter, remote_url = find_converter(repo)
        url = converter.run(repo, remote_url, path.relative_to(repo_root), args.line)

        print(url)
    except ToolError as e:
        print(e)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
