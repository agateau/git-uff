# Copyright 2021 Aurélien Gâteau <mail@agateau.com>
# SPDX-License-Identifier: Apache-2.0
from configparser import NoOptionError
from typing import Tuple, List, Iterator

from git import Repo

from git_uff.converters import Converter, get_converter_classes_dict


DEFAULT_FORGES = (
    ("github.com", "github"),
    ("gitlab.com", "gitlab"),
    ("git.sr.ht", "sourcehut"),
    ("git.zx2c4.com", "cgit"),
    ("invent.kde.org", "gitlab"),
)


def read_git_config(repo: Repo) -> Iterator[Tuple[str, str]]:
    reader = repo.config_reader()
    for section in reader.sections():
        if not section.startswith("uff "):
            continue
        url = section[5:-1]
        try:
            forge = reader.get(section, "forge")
        except NoOptionError:
            continue
        yield url, forge.lower()


def load_config(repo: Repo) -> List[Converter]:
    lst = []
    dct = get_converter_classes_dict()

    def add_forge(base_url: str, forge: str) -> None:
        try:
            converter_klass = dct[forge]
        except KeyError:
            print(f"Invalid forge '{forge}' for '{base_url}'")
            return
        lst.append(converter_klass(base_url))

    for base_url, forge in DEFAULT_FORGES:
        add_forge(base_url, forge)

    for base_url, forge in read_git_config(repo):
        add_forge(base_url, forge)

    return lst
