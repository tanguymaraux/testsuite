import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml
from dacite import from_dict

default_path = 'tests'


@dataclass
class Test:
    category: str
    tests: list = field(default_factory=None)


@dataclass
class TestCase:
    name: str
    input: str
    returncode: int = field(default=0)
    # TODO
    #category: str = field(default=None)
    todo: bool = field(default=False)
    checks: list = field(default_factory=lambda: ["stdout", "exitcode"])


def list_files(path):
    if path is None:
        path = default_path
    cur_path = Path(__file__).parent.parent.joinpath(
        path).absolute()
    files_list = []
    for root, dirs, files in os.walk(cur_path):
        for f in files:
            if f.endswith(".yaml") or f.endswith(".yml"):
                files_list.append(os.path.join(root, f))

    return files_list


def add_file(files, category):
    testsuite = {}

    for fi in files:
        with open(fi) as f:
            for cat in yaml.load(f, Loader=yaml.SafeLoader):
                new = from_dict(data_class=Test,
                                data=cat)

                if category is not None and new.category != category:
                    continue

                if new.category not in testsuite.keys():
                    testsuite[new.category] = []
                testsuite[new.category] += new.tests

    for cat, tests in testsuite.items():
        tests_list = []
        for t in tests:
            test = from_dict(data_class=TestCase, data=t)
            tests_list.append(test)

            testsuite[cat] = tests_list

    return testsuite
