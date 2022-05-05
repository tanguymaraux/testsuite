import copy
import subprocess as sp
from argparse import ArgumentParser
from dataclasses import dataclass, field
from difflib import unified_diff
from pathlib import Path

import termcolor
from alive_progress import alive_bar

import files

default_timeout = 1


def parse_arg():
    parser = ArgumentParser('Testsuite')
    parser.add_argument('-b', required=True,
                        help='path to the binary', type=Path, metavar='BINARY_PATH',)
    parser.add_argument('-p', required=False,
                        help='path to the tests directory', type=Path, metavar='TESTS_PATH',)
    parser.add_argument('-t', required=False,   metavar='TIMEOUT',
                        help='timeout of execution (seconds)', type=int)
    parser.add_argument('-c', required=False, metavar='CATEGORY',
                        help='category to test', type=str)
    parser.add_argument('-v', action='store_true',
                        help='activate verbose mode')

    return parser.parse_args()


if __name__ == "__main__":
    #args = parse_arg()
    # TODO: print credits

    #category, binary, printf = args.c, args.b, args.p
    #timeout = default_timeout if args.t is None else args.t
    files = files.list_files()
    print(files)

    #print(f"Testing binary: {binary}")

    #files = list_files()
    #testsuite = add_file(files, category)

    #print(f"Found {len(testsuite)} tests\n")

    #exit(print_tests(testsuite, printf))
