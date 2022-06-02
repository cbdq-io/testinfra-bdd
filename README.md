# testinfra-bdd

[![CI](https://github.com/locp/testinfra-bdd/actions/workflows/ci.yml/badge.svg)](https://github.com/locp/testinfra-bdd/actions/workflows/ci.yml)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/locp/testinfra-bdd.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/locp/testinfra-bdd/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/locp/testinfra-bdd.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/locp/testinfra-bdd/context:python)

An interface between
[pytest-bdd](https://pytest-bdd.readthedocs.io/en/latest/)
and
[pytest-testinfra](https://testinfra.readthedocs.io/en/latest/index.html).

## Defining Scenarios

Given a directory structure of:

```shell
"."

└── "tests"
    ├── "features"
    │   ├── "example.feature"
    └── "step_defs"
        └── "test_example.py"
```

The file `tests/features/example.feature` could look something like:

```gherkin
Feature: Example of Testinfra BDD
  Give an example of all the possible Given, When and Then steps.

  Scenario: Skip Tests if Host is Windoze
    Given the host with URL "docker://sut" is ready within 10 seconds
    # The system property can be one of:
    #   - type (e.g. linux).
    #   - distribution (e.g. debian).
    #   - release (e.g. 11).
    #   - codename (e.g. bullseye).
    #   - arch (e.g. x86_64).
    #   - hostname (e.g. sut).
    #   - connection_type (e.g. docker or ssh).
    When the system property type is not Windoze skip tests

  Scenario Outline: Test for Absent Resources
    Given the host with URL "docker://sut" is ready within 10 seconds
    When the <resource_type> is "foo"
    Then the <resource_type> is absent
    And the <resource_type> state is absent # Alternative method.
    Examples:
      | resource_type |
      | user          |
      | group         |
      | package       |
      | file          |
      | pip package   |

  Scenario: User Checks
    Given the host with URL "docker://sut" is ready
    When the user is "ntp"
    Then the user is present
    And the user state is present # Alternative method of checking the state of a resource.
    And the user group is ntp
    And the user uid is 101
    And the user gid is 101
    And the user home is /nonexistent
    And the user shell is /usr/sbin/nologin

  Scenario: File Checks
    Given the host with URL "docker://sut" is ready
    When the file is /etc/ntp.conf
    # Expected state can be present or absent.
    Then the file is present
    # Alternative method of checking the state of a resource.
    And the file state is present
    # Valid types to check for are file, directory, pipe, socket or symlink.
    And the file type is file
    And the file owner is ntp
    And the file group is ntp
    And the file contents contains "debian.pool.ntp"
    And the file contents contains the regex ".*pool [0-9].debian.pool.ntp.org iburst"
    # The expected mode must be specified as an octal.
    And the file mode is 0o544

  Scenario: Group Checks
    Given the host with URL "docker://sut" is ready
    When the group is "ntp"
    # Can check if the group is present or absent.
    Then the group is present
    # Alternative method of checking the state of a resource.
    And the group state is present
    And the group gid is 101

  Scenario: Running Commands
    Given the host with URL "docker://sut" is ready
    When the command is "ntpq -np"
    Then the command return code is 0
    And the command "ntpq" exists in path
    And the command stdout contains "remote"

  Scenario: System Package
    Given the host with URL "docker://sut" is ready
    When the package is ntp
    # Can check if the package is absent, present or installed.
    Then the package is installed

  Scenario: Python Package
    Given the host with URL "docker://sut" is ready
    When the pip package is testinfra-bdd
    # Can check if the package is absent or present.
    Then the pip package is present
    And the pip package version is 0.3.0
    # Check that installed packages have compatible dependencies.
    And the pip check is OK

  Scenario Outline: Service Checks
    Given the host with URL "docker://sut" is ready
    When the service is <service>
    Then the service is <running_state>
    And the service is <enabled_state>
    Examples:
      | service | running_state | enabled_state |
      | ntp     | running       | enabled       |
      | named   | not running   | not enabled   |

  Scenario: Test Running Processes
    Given the host with URL "docker://sut" is ready
    # Processes are selected using filter() attributes names are
    # described in the ps man page.
    When the process filter is "user=root,comm=ntpd"
    Then the process count is 1

  Scenario Outline: Test Pip Packages are Latest Versions
    Given the host with URL "docker://sut" is ready
    When the pip package is <pip_package>
    Then the pip package is present
    And the pip package is latest
    Examples:
      | pip_package      |
      | pytest-bdd       |
      | pytest-testinfra |
      | testinfra-bdd    |

  Scenario Outline:  Check Sockets
    # This checks that NTP is listening but SSH isn't.
    # The socket url is defined at https://testinfra.readthedocs.io/en/latest/modules.html#socket
    Given the host with URL "docker://sut" is ready within 10 seconds
    When the socket is <url>
    Then the socket is <expected_state>
    Examples:
      | url       | expected_state |
      | udp://123 | listening      |
      | tcp://22  | not listening  |

  Scenario: Check Network Address
    Given the host with URL "docker://sut" is ready within 10 seconds
    When the address is www.google.com
    Then the address is resolvable
    And the address is reachable

  Scenario: Check Network Address With Port
    Given the host with URL "docker://sut" is ready within 10 seconds
    When the address and port is www.google.com:443
    Then the address is resolvable
    And the address is reachable
    And the port is reachable

  Scenario: Check Java is Installed in the Path
    Given the host with URL "docker://java11" is ready within 10 seconds
    Then the command "java" exists in path

  Scenario: Check Java 11 is Installed
    Given the host with URL "docker://java11" is ready
    When the command is "java -version"
    And the package is java-11-amazon-corretto-devel
    Then the command stderr contains "Corretto-11"
    And the command stderr contains the regex "openjdk version \"11\\W[0-9]"
    And the command stdout is empty
    And the command return code is 0
    And the package is installed
```

and `tests/step_defs/test_example.py` contains the following:

```python
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
```
## "Given" Steps

Given steps require that the URL of the system to be tested (SUT) is provided.
This URL should comply to the connection string for the [Testinfra connection
string](https://testinfra.readthedocs.io/en/latest/backends.html) (e.g.
docker://my-host).  Please note that the URL _must_ be enclosed in double
quotes.

Examples:

To connect to a Docker container called sut (fail if the target host is
not ready):
```gherkin
Given the host with URL "docker://java11" is ready
```

To connect to a Docker container called sut but give it 60 seconds to become
ready, use the following:

```gherkin
Given the host with URL "docker://sut" is ready within 60 seconds
```

If the host does not become available after 60 seconds, fail the tests.

### Writing a customized "Given" Step

It may be that you may want to create a customized "Given" step.  An example
could be that the hosts to be tested may be parametrized.  The "Given" step
must return a target fixture called "testinfra_bdd_host" so that the rest of
the Testinfra BDD fixtures will function.  This fixture is a instance of the
`testinfra_bdd.`

The "Given" step should also ascertain that the target host is ready (one
can use the `is_host_ready` function for that).

An example is:

```python
from pytest_bdd import given
from testinfra_bdd import TestinfraBDD

@given('my host is ready', target_fixture='testinfra_bdd_host')
def my_host_is_ready():
    """
    Specify that the target host is a docker container called
    "my-host" and wait up to 60 seconds for the host to be ready.
    """
    host = TestinfraBDD('docker://my-host')
    assert host.is_host_ready(60), 'My host is not ready.'
    return host

...
```

## "When" Steps

When steps require that a "Given" step has been executed beforehand.  They
allow the user to either skip tests if the host does not match an expected
profile.  They also allow the user to specify which resource or is to be
tested.


### Skip Tests if Host Profile Does Not Match

It may be useful to skip tests if you find that the system under test doesn't
match an expected profile (e.g. the system is not debian as expected).  This
can be achieved by comparing against the following configurations:

- The OS Type (e.g. linux).
- The distribution name (e.g. debian).
- The OS release (e.g. 11).
- The OS codename if relevant (e.g. bullseye).
- The host architecture (e.g. x86_64).
- The hostname (e.g. sut)

Example:
```gherkin
  Scenario: Skip Tests if Host is Windoze
    Given the host with URL "docker://sut" is ready within 10 seconds
    When the system property type is not Windoze skip tests
```
