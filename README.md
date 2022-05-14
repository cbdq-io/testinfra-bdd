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

  Scenario: Start NTP Service
    Given the host with URL "docker://sut" is ready within 10 seconds
    When the command is "service ntp start"
    Then the command return code is 0

  Scenario: System Under Test
    Given the host with URL "docker://sut" is ready within 10 seconds
    When the system property type is not "linux" skip tests
    And the command is "ntpq -np"
    And the package is ntp
    And the file is /etc/ntp.conf
    Then the command return code is 0
    And the command stdout contains "remote"
    And the package is installed
    And the file is present
    And the file type is file
    And the file owner is ntp
    And the file group is ntp
    And the file contents contains "debian.pool.ntp"
    And the file contents contains the regex ".*pool [0-9].debian.pool.ntp.org iburst"
    And the file mode is 0o544

  Scenario: Skip Tests if Host is Windoze
    Given the host with URL "docker://sut" is ready within 10 seconds
    When the system property type is not Windoze skip tests

  Scenario: Check Java is Installed in the Path
    Given the host with URL "docker://java11" is ready within 10 seconds
    Then the command "java" exists in path

  Scenario: Check Java 11 is Installed
    Given the host with URL "docker://java11" is ready
    When the command is "java -version"
    And the package is java-11-amazon-corretto-devel
    Then the command stderr contains "Corretto-11"
    And the command stderr matches regex "openjdk version \"11\\W[0-9]"
    And the command stdout is empty
    And the command return code is 0
    And the package is installed

  Scenario Outline: Check a Service Status
    Given the host with URL "docker://sut" is ready
    When the service is <service_name>
    And the package is <package_name>
    And the file is <file_name>
    Then the service <status> enabled
    And the service <status> running
    And the package is <package_status>
    And the file is <file_status>
    Examples:
      | service_name | status | package_name | package_status | file_name       | file_status |
      | ntp          | is     | ntp          | installed      | /etc/ntp.conf   | present     |
      | named        | is not | named        | absent         | /etc/named.conf | absent      |

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

## "Then" Steps

### Check a Command Exists on the Path

In this example, the test will pass if the command called "java" is found
on the path of the host being tested:

```gherkin
  Scenario: Check Java is Installed in the Path
    Given the host with URL "docker://java11" is ready within 10 seconds
    Then the command java exists in path
```

### Check a Command Return Code

```gherkin
  Scenario: Start NTP Service
    Given the host with URL "docker://sut" is ready within 10 seconds
    When the command is "service ntp start"
    Then the command return code is 0
```

### Check the Output of a Command
There are two output streams for a command.  The stream called stdout is
for standard output and stderr is for the standard error.

There following methods are available:

Check for a string in the standard error:
```gherkin
Then the command stderr contains "Corretto-11"
```

Check for a regular expression in the standard error:
```gherkin
Then command stderr matches regex "openjdk version \"11\\W[0-9]"
```

Check a stream (standard output) is empty:
```gherkin
Then the command stdout is empty
```

### Check the Status of a Service

Check that a service (ntp) is running and enabled:

```gherkin
When the service is ntp
Then the service is running
And the service is enabled
```

Check that a service (named) is not running and is disabled:

```gherkin
When the service is named
Then the service is not running
And the service is not enabled
```

### Check the Installation Status of a Package

Check that a package (ntp) is installed:

```gherkin
When the package is ntp
Then the package is installed
```

This same check can also be written as:

```gherkin
When the package is ntp
Then the package is present
```

To assert that a package (named) is absent:

```gherkin
When the package is named
Then the package is absent
```

### Checking the Status of a File

Check if a file is present on the host:

```gherkin
When file is /etc/ntp.conf
Then the file is present
```

Check if a file is absent on the host:

```gherkin
When file is /etc/ntp.conf
Then the file is absent
```

Check the file type (the file type must be one of file, directory, pipe, socket
or symlink):

```gherkin
When file is /etc/ntp.conf
Then the file type is file
```

Check the name of the owner of a file:

```gherkin
When file is /etc/ntp.conf
Then the file owner is ntp
```

Check the name of the group of a file:

```gherkin
When file is /etc/ntp.conf
Then the file group is ntp
```

Search for a string in the contents of the file (the text to search for must be
enclosed in double quotes):

```gherkin
When file is /etc/ntp.conf
Then the file contents contains "debian.pool.ntp"
```

Search for a regular expression in the contents of the file (the regex must
be enclosed in double quotes):

```gherkin
When file is /etc/ntp.conf
Then the file contents contains the regex ".*pool [0-9].debian.pool.ntp.org iburst"
```

Check the permissions of a file (the permissions must be specified as Octal):

```gherkin
When file is /etc/ntp.conf
Then the file mode is 0o544
```

### Checking the Status of a User

When naming the user in the "when" step, it is optional if the name is
enclosed in double-quotes:

```gherkin
When the user is "ntp"
```

Check the user is present:

```gherkin
Then the user state is present
```

Check the user is absent:

```gherkin
Then the user state is absent
```

Check the name of the primary group of the user:

```gherkin
Then the user group is ntp
```

Check the uid of the user:

```gherkin
Then the user uid is 101
```

Check the gid of the user:

```gherkin
Then the user gid is 101
```

Check the name of the home directory of the user:

```gherkin
Then the user home is /nonexistent
```

```gherkin
Check the shell of the user:
```

```gherkin
Then the user shell is /usr/sbin/nologin
```
