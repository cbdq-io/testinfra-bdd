"""Test Scenarios That Might Allow Tests to be Skipped feature tests."""

from pytest_bdd import (
    scenario,
    then
)

# Ensure that the PyTest fixtures provided in testinfra-bdd are available to
# your test suite.
pytest_plugins = ['testinfra_bdd']


@scenario('../features/skip.feature', 'Skip Tests Due to Arch')
def test_skip_tests_due_to_arch():
    """Skip Tests Due to Arch."""


@scenario('../features/skip.feature', 'Skip Tests Due to Codename')
def test_skip_tests_due_to_codename():
    """Skip Tests Due to Arch."""


@scenario('../features/skip.feature', 'Skip Tests Due to Distribution')
def test_skip_tests_due_to_distribution():
    """Skip Tests Due to Arch."""


@scenario('../features/skip.feature', 'Skip Tests Due to Release')
def test_skip_tests_due_to_release():
    """Skip Tests Due to Arch."""


@scenario('../features/skip.feature', 'Skip Tests Due to Type')
def test_skip_tests_due_to_type():
    """Skip Tests Due to Arch."""


@scenario('../features/skip.feature', 'Skip Tests on Non-Existent Host')
def test_skip_tests_on_nonexistent_host():
    """Skip Tests on Non-Existent Host."""


@scenario('../features/skip.feature', 'Skip Tests on Non-Existent Host After Waiting')
def test_skip_tests_on_nonexistent_host_after_waiting():
    """Skip Tests on Non-Existent Host After Waiting."""


@then('raise NotImplementedError')
def raise_notimplementederror():
    """raise NotImplementedError."""
    raise NotImplementedError
