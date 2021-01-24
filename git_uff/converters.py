# Copyright 2021 Aurélien Gâteau <mail@agateau.com>
# SPDX-License-Identifier: Apache-2.0
import re

from urllib.parse import quote_plus
from pathlib import Path


class Converter:
    """A Converter turns a local path into its matching forge URL.

    The conversion is done through two class variables:
    - URL_TEMPLATE: can contain {base_url}, {project}, {branch}, {escaped_branch}, {path}
    - LINE_SUFFIX: used when --line is present. It is appended to the template
    and can contain {line}
    """
    URL_TEMPLATE = ""
    LINE_SUFFIX = ""

    def __init__(self, base_url):
        self.base_url = base_url

    def match(self, remote_url: str) -> bool:
        """Returns true if this remote URL matches this converter"""
        return self.base_url in remote_url

    def run(self, remote_url: str, branch: str, path: Path, line: int = None) -> str:
        """Returns the URL for the specified path"""
        dct = {
            "base_url": self.base_url,
            "project": self.get_project(remote_url),
            "branch": branch,
            "path": path,
            "escaped_branch": quote_plus(branch),
        }

        url = self.URL_TEMPLATE.format(**dct)
        if line is not None:
            url += self.LINE_SUFFIX.format(line=line)
        return url

    def get_project(self, remote_url: str) -> str:
        """Takes an URL of the form "https://{base_url}/foo/bar.git" or
        "git@{base_url}:foo/bar.git" and returns "foo/bar".
        """
        _, project = re.split(re.escape(self.base_url) + "[:/]", remote_url)
        return project.replace(".git", "")


class GitHubConverter(Converter):
    URL_TEMPLATE = "https://{base_url}/{project}/blob/{branch}/{path}"
    LINE_SUFFIX = "#L{line}"


GitLabConverter = GitHubConverter


class SourceHutConverter(Converter):
    URL_TEMPLATE = "https://{base_url}/{project}/tree/{branch}/{path}"
    LINE_SUFFIX = "#L{line}"


class CGitConverter(Converter):
    URL_TEMPLATE = "https://{base_url}/{project}/tree/{path}?h={escaped_branch}"
    LINE_SUFFIX = "#n{line}"
