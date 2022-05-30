"""
Examples of step definitions for Testinfra BDD feature tests.

Notes
-----
The user must define their scenarios in a way similar to below.  However, the
scenarios can be empty.
"""

from pytest_bdd import scenario

# Ensure that the PyTest fixtures provided in testinfra-bdd are available to
# your test suite.
pytest_plugins = ['testinfra_bdd']


@scenario('../features/example.feature', 'Start NTP Service')
def test_start_ntp_service():
    """Start NTP Service."""


@scenario('../features/example.feature', 'Check Java 11 is Installed')
def test_check_java_11_is_installed():
    """Check Java 11 is Installed."""


@scenario('../features/example.feature', 'Check Java is Installed in the Path')
def test_check_java_is_installed_in_the_path():
    """Check Java is Installed in the Path."""


@scenario('../features/example.feature', 'Skip Tests if Host is Windoze')
def test_skip_tests_if_host_is_windoze():
    """Skip Tests if Host is Windoze."""


@scenario('../features/example.feature', 'System Under Test')
def test_system_under_test():
    """System Under Test."""


@scenario('../features/example.feature', 'Check a Service Status')
def test_check_a_service_status():
    """Check a Service Status."""


@scenario('../features/example.feature', 'Test for Absent Resources')
def test_test_for_absent_resources():
    """Test for Absent Resources."""
