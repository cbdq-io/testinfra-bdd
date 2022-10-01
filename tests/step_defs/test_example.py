"""Examples of step definitions for Testinfra BDD feature tests."""
import testinfra_bdd
from pytest_bdd import given, scenarios

scenarios('../features/example.feature')


# Ensure that the PyTest fixtures provided in testinfra-bdd are available to
# your test suite.
pytest_plugins = testinfra_bdd.PYTEST_MODULES


@given('the expected value is "foo"', target_fixture='expected_value')
def the_expected_value_is_foo():
    """
    The expected value is "foo".

    The name and code is up to the user to develop.  However, the target
    fixture must be called 'expected_value'.
    """
    return 'foo'
