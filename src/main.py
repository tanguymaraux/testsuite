from argparse import ArgumentParser
from pathlib import Path

import files as Files
import testsuite as Ts

default_timeout = 2


def parse_arg():
    """Parse arguments

    :return: arguments
    :rtype: argparse.Namespace
    """
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
    print(f"\nGeneral testsuite for your programs.\nMIT License, Copyright (c) 2022 Tanguy Maraux,\ngithub.com/tanguymaraux/testsuite\n")

    args = parse_arg()
    path = args.p
    category, binary, verbose = args.c, args.b, args.v
    timeout = default_timeout if args.t is None else args.t
    files = Files.list_files(path)

    print(f"Testing binary: \'{binary}\'")
    print(f"Tests directory: \'{path}\'")

    tests = Files.add_file(files, category)
    testsuite = Ts.Testsuite()

    # number of tests
    count = sum(len(cat) for cat in tests.values())

    # Run all tests
    exit(testsuite.run_tests(tests, binary, timeout, count, verbose))
