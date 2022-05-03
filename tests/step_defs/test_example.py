"""Example of Testinfra BDD feature tests."""

from pytest_bdd import scenario

# Ensure that the PyTest fixtures provided in testinfra-bdd are available to
# your test suite.
pytest_plugins = ['testinfra_bdd']


@scenario('../features/example.feature', 'System Under Test')
def test_system_under_test():
    """System Under Test."""
