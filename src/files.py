import os
from pathlib import Path

import yaml
from dacite import from_dict

default_path = 'tests'


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
    categories, testsuite = [], []
    cur_path = os.path.dirname(os.path.abspath(__file__))
    for fi in files:
        with open(os.path.join(cur_path, fi)) as f:
            for cat in yaml.load(f, Loader=yaml.SafeLoader):
                categories.append(from_dict(data_class=Category, data=cat))

    for cat in (cat for cat in categories if (category is None) or (category is not None and cat.category == category)):
        for t in cat.tests:
            test = from_dict(data_class=TestCase, data=t)
            test.category = cat.category
            if test.file == None:
                dir_path = tests_path + "/" + test.directory
                for f in os.listdir(dir_path):
                    file_path = dir_path + "/" + f
                    if os.path.isfile(file_path) and os.path.splitext(file_path)[1] == ".tig":
                        test_copy = copy.deepcopy(test)
                        test_copy.file = file_path
                        testsuite.append(test_copy)
            else:
                test.file = tests_path + "/" + test.directory + "/" + test.file
                testsuite.append(test)
    return testsuite
