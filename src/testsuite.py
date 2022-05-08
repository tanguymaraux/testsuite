import os
import subprocess as sp
from difflib import unified_diff

import termcolor
from alive_progress import alive_bar

PASSED = termcolor.colored('Passed', 'green')
SUMMARY = termcolor.colored('Summary', 'yellow')
FAILED = termcolor.colored('Failed', 'red')
TODO = termcolor.colored('Todo', 'cyan')
TIMEOUT = termcolor.colored('Timeout', 'red')
TESTS = termcolor.colored('tests', 'yellow')
PASS_LINE = termcolor.colored('=================', 'yellow')
OK = termcolor.colored('OK', 'green')
OK_line = termcolor.colored('=================', 'green')
KO = termcolor.colored('KO', 'red')
KO_line = termcolor.colored('=================', 'red')
TO = termcolor.colored('TIMED OUT', 'red')
KORE = termcolor.colored('KO - RECOMPILE FAIL', 'red')
CAT_line = termcolor.colored('=================', 'cyan')
FL_line = termcolor.colored('=================', 'magenta')


class Testsuite:
    def diff(self, expected: str, actual: str):
        # TODO: add diff
        expected_out = expected.splitlines(keepends=True)
        actual_out = actual.splitlines(keepends=True)
        return ''.join(unified_diff(expected_out, actual_out, fromfile='expected', tofile='actual'))

    def run(self, binary: str, timeout: int, testcase):
        try:
            exe = ["bash", binary]
            exe += testcase.input.split(" ")
            return sp.run(exe, capture_output=True, text=True, timeout=timeout)
        except sp.TimeoutExpired:  # check time out
            self.timeout += 1
            print(f"{KO_line} [ {TO} ] {testcase.name} {KO_line}")
            return None

    def check(self, actual: sp.CompletedProcess, testcase):
        failed = False
        file_name = os.path.basename(actual.args[1])

        if actual.returncode != testcase.returncode:
            failed = True
            print(f"{KO_line}{KO_line}{KO_line}")
            print(
                f"Expected returncode {testcase.returncode}, got {actual.returncode}")
            print(f"Stderr: {actual.stderr}")

    #    if "has_stderr" in checks and actual.stderr == "":
            # print(f"{KO_line}{KO_line}{KO_line}")
    #        failed = True
    #        print("Something was expected on stderr")
    #
    #    if "stdout" in testcase.checks and testcase.stdout != actual.stdout:
            # print(f"{KO_line}{KO_line}{KO_line}")
    #        failed = True
    #        print(f"Stdout differ\n{diff(testcase.stdout, actual.stdout)}")
    #
    #    if "stderr" in checks and expected.stderr != actual.stderr:
            # print(f"{KO_line}{KO_line}{KO_line}")
    #        failed = True
    #        print(f"Stderr differ\n{diff(expected.stderr, actual.stderr)}")

        assert not failed

    def print_test(self, bin_proc, testcase):
        try:
            self.check(bin_proc, testcase)
        except AssertionError as e:
            self.failed = True
            self.nb_failed += 1
            print(f"{KO_line} [ {KO} ] {testcase.name} {KO_line}\n {e}")
        else:
            if self.verbose:
                self.nb_passed += 1
                print(f"{OK_line} [ {OK} ] {testcase.name} {OK_line}")

    def run_tests(self, testsuite, binary, timeout, nb_tests, verbose):
        self.failed, self.nb_failed, self.verbose, self.timeout, self.todo, self.nb_passed = False, 0, verbose, 0, 0, 0

        with alive_bar(nb_tests) as bar:
            for cat in testsuite.keys():
                if verbose:
                    print(f"\n{CAT_line} Category: {cat}")
                for testcase in testsuite[cat]:
                    if not testcase.todo:
                        bin_proc = self.run(binary, timeout, testcase)
                        self.print_test(bin_proc, testcase)
                    else:
                        self.todo += 1

                    bar()  # update progress bar

        print(
            f"\n{PASS_LINE} {SUMMARY} - Passed: [{nb_tests - self.nb_failed}/{nb_tests}] {PASS_LINE}")
        print(f"# {PASSED}: {self.nb_passed}")
        print(f"# {FAILED}: {self.nb_failed}")
        print(f"# {TIMEOUT}: {self.timeout}")
        print(f"# {TODO}: {self.todo}")
        print(
            f"# Total: {self.nb_failed + self.timeout + self.todo + (self.nb_passed)}\n")

        return self.failed
