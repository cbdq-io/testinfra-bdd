"""The when steps of testinfra-bdd."""
import os
import pytest
from pytest_bdd import parsers
from pytest_bdd import when


@when(parsers.parse('the system property {property_name} is not "{expected_value}" skip tests'))
@when(parsers.parse('the system property {property_name} is not {expected_value} skip tests'))
def skip_tests_if_system_info_does_not_match(property_name, expected_value, testinfra_bdd_host):
    """
    Skip tests if a system property does not patch the expected value.

    Parameters
    ----------
    property_name : str
    expected_value : str
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.
    """
    actual_value = testinfra_bdd_host.get_host_property(property_name)
    if actual_value != expected_value:
        pytest.skip(f'System {property_name} is {actual_value} which is not {expected_value}.')


@when(parsers.parse('the environment variable {key} is {value} skip tests'))
def skip_tests_if_env_key_is(key, value):
    """
    Skip tests if an environment variable is set to a particular value.

    Parameters
    ----------
    key : str
        The name of the environment variable.
    value : str
        The value the environment variable must be for the tests to be skipped.
    """
    if key in os.environ and os.environ[key] == value:
        pytest.skip(f'Environment variable {key} is set to {value}.')
