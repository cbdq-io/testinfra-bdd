"""Fix Issue 21 feature tests."""

from pytest_bdd import scenario

# Ensure that the PyTest fixtures provided in testinfra-bdd are available to
# your test suite.
pytest_plugins = ['testinfra_bdd']


@scenario('../features/issue21.feature', 'Issue 21')
def test_issue_21():
    """Issue 21."""
