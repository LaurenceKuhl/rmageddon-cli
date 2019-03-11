#!/usr/bin/env python
"""Some tests covering the linting code.
Provide example project contents like:

    --tests
            |--lint_examples
            |     |--example_project1
            |     |     |...<files here>
            |     |--example_project2
            |     |     |....<files here>
            |     |...
            |--test_lint.py
"""
import os
import sys

import unittest
from ruamel.yaml import YAML
import rmageddon.lint as lint


def listfiles(path):
    files_found = []
    for (_, _, files) in os.walk(path):
        files_found.extend(files)
    return files_found


def pf(wd, path):
    return os.path.join(wd, path)


WD = os.path.dirname(__file__)
PATH_MINIMAL_WORKING_EXAMPLE = pf(WD, "lint_examples/minimal_working_example")
PATH_OPTIMAL_WORKING_EXAMPLE = pf(WD, "lint_examples/awesome_working_example")
PATH_BAD_EXAMPLE = pf(WD, "lint_examples/bad_example")
PATH_BAD_DOCKERFILE = pf(WD, "lint_examples/corrupt_dockerfile_example")
PATH_INCOMPLETE_DOCKERFILE = pf(WD, "lint_examples/missing_label_dockerfile_example")
# The maximum number of checks that can be passed
MAX_PASS_CHECKS = 7


class TestLint(unittest.TestCase):
    """ Class for lint tests """

    def assess_lint_status(self, lint_obj, **expected):
        """Little helper function for assessing the lint
        object status lists"""
        for list_type, expect in expected.items():
            observed = len(getattr(lint_obj, list_type))
            yaml = YAML(typ='safe')
            observed_list = yaml.dump(getattr(lint_obj, list_type), sys.stdout)
            self.assertEqual(observed, expect, "Expected {} tests in '{}', \
                but found {}.\n{}".format(expect, list_type.upper(), observed, observed_list))

    def test_read_dir_content_and_pass(self):
        """ Check if the dir contains several files/dirs.
            Minimal example for passing.

            Fails if not present: Dockerfile, environment.yml
            Warns if not present: scripts, data
        """
        lint_obj = lint.RContainerLint(PATH_MINIMAL_WORKING_EXAMPLE)
        lint_obj.lint_rproject()
        expectations = {"failed": 0, "warned": 2, "passed": MAX_PASS_CHECKS - 2}
        self.assess_lint_status(lint_obj, **expectations)

    def test_read_dir_ultimate_content_and_pass(self):
        """ Check if the dir contains several files/dirs.
            Optimal example for passing.

            Fails if not present: Dockerfile, rpackages.txt
            Warns if not present: scripts, data
        """
        lint_obj = lint.RContainerLint(PATH_OPTIMAL_WORKING_EXAMPLE)
        lint_obj.lint_rproject()
        expectations = {"failed": 0, "warned": 0, "passed": MAX_PASS_CHECKS}
        self.assess_lint_status(lint_obj, **expectations)

    def test_dockerfile_with_wrong_base_image(self):
        """ Check if a Dockerfile has the correct base image
        included from r-base 
        """
        lint_obj = lint.RContainerLint(PATH_BAD_EXAMPLE)
        lint_obj.check_dockerfile()
        expectations = {"failed": 1, "warned": 0, "passed": 0}
        self.assess_lint_status(lint_obj, **expectations)

    def test_dockerfile_without_base_image(self):
        """ Check if a Dockerfile has a base image
        included from r-base 
        """
        lint_obj = lint.RContainerLint(PATH_BAD_DOCKERFILE)
        lint_obj.lint_rproject()
        expectations = {"failed": 1, "warned": 2, "passed": 1}
        self.assess_lint_status(lint_obj, **expectations)

    def test_rpackage_empty_warn(self):
        """ Check if the rpackages.txt is empty """
        lint_obj = lint.RContainerLint(PATH_BAD_EXAMPLE)
        lint_obj.check_dockerfile()
        expectations = {"failed": 1, "warned": 0, "passed": 0}
        self.assess_lint_status(lint_obj, **expectations)

    def test_rpackage_pass(self):
        """ Check if the rpackages.txt is formatted correctly """
        lint_obj = lint.RContainerLint(PATH_MINIMAL_WORKING_EXAMPLE)
        lint_obj.check_dockerfile()
        expectations = {"failed": 0, "warned": 0, "passed": 2}
        self.assess_lint_status(lint_obj, **expectations)

    def test_labels_are_defined_properly_fail(self):
        """ Check that the LABELs are set properly in the Dockerfile
        We expect to have:
            - name
            - maintainer
            - version
            - organization
            - github
        set.
        """
        lint_obj = lint.RContainerLint(PATH_INCOMPLETE_DOCKERFILE)
        lint_obj.check_dockerfile()
        expectations = {"failed": 1, "warned": 0, "passed": 1}
        self.assess_lint_status(lint_obj, **expectations)

    def test_conda_env_file_for_name_and_fail(self):
        """ Check that the conda env file has a name property and that it
        follows a certain regex, fail if not """
        lint_obj = lint.RContainerLint(PATH_BAD_EXAMPLE)
        lint_obj.check_conda_environment()
        expectations = {"failed": 1, "warned": 0, "passed": 0}
        self.assess_lint_status(lint_obj, **expectations)

    def test_conda_env_file_for_channels_and_fail(self):
        """ Check that the conda env file has a name property and that it
        follows a certain regex, fail if not """
        lint_obj = lint.RContainerLint(PATH_BAD_EXAMPLE)
        lint_obj.check_conda_environment()
        expectations = {"failed": 1, "warned": 0, "passed": 0}
        self.assess_lint_status(lint_obj, **expectations)

    def test_conda_env_file_no_rversion_tag(self):
        """ Check that the conda env file has a name property and that it
        follows a certain regex, fail if not """
        lint_obj = lint.RContainerLint(PATH_BAD_EXAMPLE)
        lint_obj.check_files_exist()
        yaml = YAML()
        lint_obj.conda_config = yaml.load(
            """
            name: qbicsoftware-QTEST-ranalyses-1.0
            channels:
                - bioconda
                - r
                - defaults
            dependencies:
                - r-base
                - r-ggplot2
            """
        )
        lint_obj.check_conda_environment()
        expectations = {"failed": 1, "warned": 2, "passed": 2}
        self.assess_lint_status(lint_obj, **expectations)

    def test_conda_env_file_wrong_rversion_tag(self):
        """ Check that the conda env file has a name property and that it
        follows a certain regex, fail if not """
        lint_obj = lint.RContainerLint(PATH_BAD_EXAMPLE)
        lint_obj.check_files_exist()
        yaml = YAML()
        lint_obj.conda_config = yaml.load(
            """
            name: qbicsoftware-QTEST-ranalyses-1.0
            channels:
                - bioconda
                - r
                - defaults
            dependencies:
                - r-base=1.0dev
                - r-ggplot2
            """
        )
        lint_obj.check_conda_environment()
        expectations = {"failed": 1, "warned": 2, "passed": 2}
        self.assess_lint_status(lint_obj, **expectations)
