"""Fix Issue 21 feature tests."""
from pytest_bdd import scenarios

import testinfra_bdd

scenarios('../features/issue21.feature')

# Ensure that the PyTest fixtures provided in testinfra-bdd are available to
# your test suite.
pytest_plugins = testinfra_bdd.PYTEST_MODULES
