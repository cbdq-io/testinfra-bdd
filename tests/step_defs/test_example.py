"""Examples of step definitions for Testinfra BDD feature tests."""
import os
import pytest

from pytest_bdd import given
from pytest_bdd import scenarios

scenarios('../features/example.feature')


# Ensure that the PyTest fixtures provided in testinfra-bdd are available to
# your test suite.
pytest_plugins = ['testinfra_bdd']


@given('on GitHub Actions we skip tests')
def on_github_actions_we_skip_tests():
    """on GitHub Actions we skip tests."""
    if 'GITHUB_ACTIONS' in os.environ and os.environ['GITHUB_ACTIONS'] == 'true':
        pytest.skip('GitHub Actions does not support Ping/ICMP.')
