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
    todo: bool = field(default=False)
    has_stderr: bool = field(default=False)


def list_files(path):
    """
    List all yml files in the given path.

    :param path: path to the directory
    :type path: str

    :return: list of files
    :rtype: list
    """
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
    """
    Add all tests in the test files to a dictionnary. If the category is given, only add tests from this category.

    :param files: list of files
    :type files: list
    :param category: category to test
    :type category: str

    :return: dictionary of tests
    :rtype: dict
    """
    testsuite = {}

    for fi in files:
        with open(fi) as f:
            for cat in yaml.load(f, Loader=yaml.SafeLoader):
                # Create a test object from the yaml file
                new = from_dict(data_class=Test,
                                data=cat)

                # Check the category
                if category is not None and new.category != category:
                    continue

                if new.category not in testsuite.keys():
                    testsuite[new.category] = []
                testsuite[new.category] += new.tests

    for cat, tests in testsuite.items():
        tests_list = []
        for t in tests:
            # Create a test case object
            test = from_dict(data_class=TestCase, data=t)
            tests_list.append(test)

            testsuite[cat] = tests_list

    return testsuite
