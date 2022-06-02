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


@scenario('../features/example.feature', 'Check Java 11 is Installed')
def test_check_java_11_is_installed():
    """Check Java 11 is Installed."""


@scenario('../features/example.feature', 'Check Java is Installed in the Path')
def test_check_java_is_installed_in_the_path():
    """Check Java is Installed in the Path."""


@scenario('../features/example.feature', 'Check Network Address')
def test_check_network_address():
    """Check Network Address."""


@scenario('../features/example.feature', 'Check Network Address With Port')
def test_check_network_address_with_port():
    """Check Network Address With Port."""


@scenario('../features/example.feature', 'Check Sockets')
def test_check_sockets():
    """Check Sockets."""


@scenario('../features/example.feature', 'File Checks')
def test_file_checks():
    """File Checks."""


@scenario('../features/example.feature', 'Group Checks')
def test_group_checks():
    """Group Checks."""


@scenario('../features/example.feature', 'Python Package')
def test_python_package():
    """Python Package."""


@scenario('../features/example.feature', 'Running Commands')
def test_running_commands():
    """Running Commands."""


@scenario('../features/example.feature', 'Service Checks')
def test_service_checks():
    """Service Checks."""


@scenario('../features/example.feature', 'Skip Tests if Host is Windoze')
def test_skip_tests_if_host_is_windoze():
    """Skip Tests if Host is Windoze."""


@scenario('../features/example.feature', 'System Package')
def test_system_package():
    """System Package."""


@scenario('../features/example.feature', 'Test Pip Packages are Latest Versions')
def test_test_pip_packages_are_latest_versions():
    """Test Pip Packages are Latest Versions."""


@scenario('../features/example.feature', 'Test Running Processes')
def test_test_running_processes():
    """Test Running Processes."""


@scenario('../features/example.feature', 'Test for Absent Resources')
def test_test_for_absent_resources():
    """Test for Absent Resources."""


@scenario('../features/example.feature', 'User Checks')
def test_user_checks():
    """User Checks."""
