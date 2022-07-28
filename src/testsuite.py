import os
import subprocess as sp
from difflib import unified_diff

import termcolor
from alive_progress import alive_bar

PASSED = termcolor.colored('Passed', 'green')
SUMMARY = termcolor.colored('Summary', 'yellow')
FAILED = termcolor.colored('Failed', 'red')
TODO = termcolor.colored('Todo', 'cyan')
TODO_line = termcolor.colored('============', 'cyan')
TIMEOUT = termcolor.colored('Timeout', 'red')
PASS_LINE = termcolor.colored('============', 'yellow')
OK = termcolor.colored('OK', 'green')
OK_line = termcolor.colored('============', 'green')
KO = termcolor.colored('KO', 'red')
KO_line = termcolor.colored('============', 'red')
KO_lineUp = termcolor.colored('^^^^^^^^^^^^', 'red')
KO_lineDown = termcolor.colored('vvvvvvvvvvvv', 'red')
TO = termcolor.colored('TIMED OUT', 'red')
KORE = termcolor.colored('KO - RECOMPILE FAIL', 'red')
CAT_line = termcolor.colored('>>>', 'magenta')


class Testsuite:
    # If you want to change the testsuite, this function may be useful
    def diff(self, expected: str, actual: str):
        """
        Compares two string and returns a list of differences

        :param expected: the expected string
        :param actual: the actual string

        :return: List of differences
        :rtype: str
        """
        expected_out = expected.splitlines(keepends=True)
        actual_out = actual.splitlines(keepends=True)

        return ''.join(unified_diff(expected_out, actual_out, fromfile='expected', tofile='actual'))

    def run(self, binary: str, timeout: int, testcase):
        """
        Runs a testcase and returns the result

        :param binary: the binary to run
        :type binary: str
        :param timeout: the timeout for the test
        :type timeout: int
        :param testcase: the testcase to run
        :type testcase: Testcase

        :return: the result of the test
        :rtype: sp.CompletedProcess
        """
        try:
            exe = ["bash", binary]
            exe += testcase.input.split(" ")

            return sp.run(exe, capture_output=True, text=True, timeout=timeout)
        except sp.TimeoutExpired:  # check time out
            self.timeout += 1
            print(f"{KO_line} [ {TO} ] {testcase.name}")

            return None

    def check(self, actual: sp.CompletedProcess, testcase):
        """
        Checks the result of a testcase

        :param actual: the result of the test
        :type actual: sp.CompletedProcess
        :param testcase: the testcase to check
        :type testcase: Testcase

        :raises AssertionError: if the result of the test is not as expected

        :return: True if the test passed, False otherwise
        :rtype: bool
        """
        failed = False

        if actual.returncode != testcase.returncode:
            failed = True
            print(f"{KO_lineDown}")
            print(
                f"Expected returncode {testcase.returncode}, got {actual.returncode}")
            if actual.stderr:
                print(f"Stderr: {actual.stderr}")

        if testcase.has_stderr and actual.stderr == "":
            print(f"{KO_lineDown}")
            failed = True
            print("Something was expected on stderr")

        assert not failed

    def print_test(self, bin_proc, testcase):
        """
        Prints the result of a testcase

        :param bin_proc: the result of the test
        :type bin_proc: sp.CompletedProcess
        :param testcase: the testcase to print
        :type testcase: Testcase
        """
        try:
            self.check(bin_proc, testcase)
        except AssertionError as e:
            self.failed = True
            self.nb_failed += 1
            print(f"{KO_lineUp} [ {KO} ] {testcase.name}\n {e}")
        else:
            self.nb_passed += 1
            if self.verbose:
                print(f"{OK_line} [ {OK} ] {testcase.name}")

    def run_tests(self, testsuite, binary, timeout, nb_tests, verbose):
        """
        Runs all tests in the testsuite and prints the result

        :param testsuite: the list of tests to run
        :type testsuite: dict
        :param binary: the binary to run
        :type binary: str
        :param timeout: the timeout for the test
        :type timeout: int
        :param nb_tests: the number of tests to run
        :type nb_tests: int
        :param verbose: if true, prints the result of each test
        :type verbose: bool

        :return: the number of tests that failed
        :rtype: int
        """
        self.failed, self.nb_failed, self.verbose, self.timeout, self.todo, self.nb_passed = False, 0, verbose, 0, 0, 0

        print(f"\n{PASS_LINE} Running {nb_tests} tests {PASS_LINE}")

        with alive_bar(nb_tests) as bar:
            for cat in testsuite.keys():
                if verbose:
                    print(f"\n{CAT_line} Category: {cat}")
                for testcase in testsuite[cat]:
                    if testcase.todo is not None and not testcase.todo:
                        bin_proc = self.run(binary, timeout, testcase)
                        if bin_proc is not None:
                            self.print_test(bin_proc, testcase)
                    else:
                        if verbose:
                            print(
                                f"{TODO_line} [ {TODO} ] {testcase.name}\n")
                        self.todo += 1

                    bar()  # update progress bar

        print(
            f"\n{PASS_LINE} {SUMMARY} - Passed: [{self.nb_passed}/{nb_tests}] {PASS_LINE}")
        print(f"# {PASSED}: {self.nb_passed}")
        print(f"# {FAILED}: {self.nb_failed}")
        print(f"# {TIMEOUT}: {self.timeout}")
        print(f"# {TODO}: {self.todo}")
        print(
            f"# Total: {self.nb_failed + self.timeout + self.todo + (self.nb_passed)}\n")

        return self.failed + self.timeout
