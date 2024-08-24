# testinfra-bdd

[![CI](https://github.com/cbdq-io/testinfra-bdd/actions/workflows/ci.yml/badge.svg)](https://github.com/cbdq-io/testinfra-bdd/actions/workflows/ci.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/5482c55d78b369a0a55e/maintainability)](https://codeclimate.com/github/cbdq-io/testinfra-bdd/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/5482c55d78b369a0a55e/test_coverage)](https://codeclimate.com/github/cbdq-io/testinfra-bdd/test_coverage)
[![testinfra-bdd](https://snyk.io/advisor/python/testinfra-bdd/badge.svg)](https://snyk.io/advisor/python/testinfra-bdd)

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

  The Given steps to skip the address and port tests when running under
  GitHub actions are not part of the testinfra-bdd package itself, but are
  required as GitHub/Azure does not allow Ping/ICMP traffic.

  Scenario: Skip Tests if Host is Windoze
    Given the TestInfra host with URL "docker://sut" is ready within 10 seconds
    # The system property can be one of:
    #   - type (e.g. linux).
    #   - distribution (e.g. debian).
    #   - release (e.g. 11).
    #   - codename (e.g. bullseye).
    #   - arch (e.g. x86_64).
    #   - hostname (e.g. sut).
    #   - connection_type (e.g. docker or ssh).
    When the TestInfra system property type is not Windoze skip tests

  Scenario Outline: Test for Absent Resources
    Given the TestInfra host with URL "docker://sut" is ready within 10 seconds
    When the TestInfra <resource_type> is "foo"
    Then the TestInfra <resource_type> is absent
    Examples:
      | resource_type |
      | user          |
      | group         |
      | package       |
      | file          |
      | pip package   |

  Scenario Outline: Test for Absent Non-Quoted Resources
    # Same as the example above except the resources are not quoted.
    Given the TestInfra host with URL "docker://sut" is ready within 10 seconds
    When the TestInfra <resource_type> is foo
    Then the TestInfra <resource_type> state is absent
    Examples:
      | resource_type |
      | user          |
      | group         |
      | package       |
      | file          |
      | pip package   |

  Scenario: User Checks
    Given the TestInfra host with URL "docker://sut" is ready
    When the TestInfra user is "ntp"
    Then the TestInfra user is present
    # Alternative method of checking the state of a resource.
    And the TestInfra user state is present
    And the TestInfra user group is ntp
    And the TestInfra user uid is 101
    And the TestInfra user gid is 101
    And the TestInfra user home is /nonexistent
    And the TestInfra user shell is /usr/sbin/nologin

  Scenario: File Checks
    Given the TestInfra host with URL "docker://sut" is ready
    When the TestInfra file is /etc/ntp.conf
    # Expected state can be present or absent.
    Then the TestInfra file is present
    # Alternative method of checking the state of a resource.
    And the TestInfra file state is present
    # Valid types to check for are file, directory, pipe, socket or symlink.
    And the TestInfra file type is file
    And the TestInfra file owner is ntp
    And the TestInfra file group is ntp
    And the TestInfra file contents contains "debian.pool.ntp"
    And the TestInfra file contents contains the regex ".*pool [0-9].debian.pool.ntp.org iburst"
    # The expected mode must be specified as an octal.
    And the TestInfra file mode is 0o544

  Scenario: File Executable Checks
    Given the TestInfra host with URL "docker://sut" is ready
    When the TestInfra file is /bin/ls
    Then the TestInfra file is present
    And the TestInfra file is executable

  Scenario: Group Checks
    Given the TestInfra host with URL "docker://sut" is ready
    When the TestInfra group is "ntp"
    # Can check if the group is present or absent.
    Then the TestInfra group is present
    # Alternative method of checking the state of a resource.
    And the TestInfra group state is present
    And the TestInfra group gid is 101

  Scenario: Group Membership
    Given the TestInfra host with URL "docker://sut" is ready
    When the TestInfra group is "sudo"
    And the TestInfra user is "bar"
    Then the TestInfra group contains the user "bar"
    And the TestInfra user groups include "sudo"

  Scenario: Running Commands
    Given the TestInfra host with URL "docker://sut" is ready
    When the TestInfra command is "ntpq -np"
    Then the TestInfra command return code is 0
    And the TestInfra command "ntpq" exists in path
    And the TestInfra command stdout contains "remote"
    And the TestInfra command stdout does not contain "foo"

  Scenario: System Package
    Given the TestInfra host with URL "docker://sut" is ready
    When the TestInfra package is ntp
    # Can check if the package is absent, present or installed.
    Then the TestInfra package is installed
    And the TestInfra package version will be greater than or equal to 1:4.2.8p15+dfsg-1

  Scenario: Python Package
    Given the TestInfra host with URL "docker://sut" is ready
    When the TestInfra pip package is testinfra-bdd
    # Can check if the package is absent or present.
    Then the TestInfra pip package is present
    And the TestInfra pip package version is 3.0.5
    And the TestInfra pip package version will be greater than or equal to 3.0.5
    # Check that installed packages have compatible dependencies.
    And the TestInfra pip check is OK

  Scenario Outline: Service Checks
    Given the TestInfra host with URL "docker://sut" is ready
    When the TestInfra service is <service>
    Then the TestInfra service is <running_state>
    And the TestInfra service is <enabled_state>
    Examples:
      | service | running_state | enabled_state |
      | ntp     | running       | enabled       |
      | named   | not running   | not enabled   |

  Scenario: Test Running Processes
    Given the TestInfra host with URL "docker://sut" is ready
    # Processes are selected using filter() attributes names are
    # described in the ps man page.
    When the TestInfra process filter is "user=root,comm=ntpd"
    Then the TestInfra process count is 1

  Scenario Outline: Test Pip Packages are Latest Versions
    Given the TestInfra host with URL "docker://sut" is ready
    When the TestInfra pip package is <pip_package>
    Then the TestInfra pip package is present
    And the TestInfra pip package is <status>
    Examples:
      | pip_package      | status |
      | pytest-bdd       | latest |
      | pytest-testinfra | latest |
      | testinfra-bdd    | latest |

  Scenario Outline:  Check Sockets
    # This checks that NTP is listening but SSH isn't.
    # The socket url is defined at https://testinfra.readthedocs.io/en/latest/modules.html#socket
    Given the TestInfra host with URL "docker://sut" is ready within 10 seconds
    When the TestInfra socket is <url>
    Then the TestInfra socket is <expected_state>
    Examples:
      | url       | expected_state |
      | udp://123 | listening      |
      | tcp://22  | not listening  |

  Scenario: Skip Tests Due to Environment Variable
    Given the TestInfra host with URL "docker://java11" is ready
    When the TestInfra environment variable PYTHONPATH is .:.. skip tests

  Scenario: Check Network Address
    Given the TestInfra host with URL "docker://sut" is ready within 10 seconds
    When the TestInfra environment variable GITHUB_ACTIONS is true skip tests
    And the TestInfra address is www.google.com
    Then the TestInfra address is resolvable
    And the TestInfra address is reachable

  Scenario: Check Network Address With Port
    Given the TestInfra host with URL "docker://sut" is ready within 10 seconds
    When the TestInfra environment variable GITHUB_ACTIONS is true skip tests
    And the TestInfra address and port is www.google.com:443
    Then the TestInfra address is resolvable
    And the TestInfra address is reachable
    And the TestInfra port is reachable

  Scenario: Check Java is Installed in the Path
    Given the TestInfra host with URL "docker://java11" is ready within 10 seconds
    Then the TestInfra command "java" exists in path

  Scenario: Check Java 11 is Installed
    Given the TestInfra host with URL "docker://java11" is ready
    When the TestInfra command is "java -version"
    And the TestInfra package is java-11-amazon-corretto-devel
    Then the TestInfra command stderr contains "Corretto-11"
    And the TestInfra command stderr contains the regex "openjdk version \"11\\W[0-9]"
    And the TestInfra command stdout is empty
    And the TestInfra command return code is 0
    And the TestInfra package is installed

  Scenario: Check for an Expected Value
   # In this example we set the expected_value to "foo"
   Given the TestInfra host with URL "docker://sut" is ready
   And the TestInfra expected value is "foo"
   When the TestInfra command is "echo foo"
   Then the TestInfra command stdout contains the expected value

  Scenario Outline: Check Contents of JSON File With JMESPath
    Given the TestInfra host with URL "docker://sut" is ready
    When the TestInfra file is /tmp/john-smith.json
    Then the TestInfra JMESPath expression <expression> returns <expected_value>
    Examples:
      | expression    | expected_value |
      | firstName     | John           |
      | lastName      | Smith          |
      | age           | 27             |
      | address.state | NY             |
      | spouse        | None           |
```

and `tests/step_defs/test_example.py` contains the following:

```python
"""Examples of step definitions for Testinfra BDD feature tests."""
import testinfra_bdd
from pytest_bdd import given, scenarios

scenarios('../features/example.feature')


# Ensure that the PyTest fixtures provided in testinfra-bdd are available to
# your test suite.
pytest_plugins = testinfra_bdd.PYTEST_MODULES


@given('the TestInfra expected value is "foo"', target_fixture='expected_value')
def the_expected_value_is_foo():
    """
    The expected value is "foo".

    The name and code is up to the user to develop.  However, the target
    fixture must be called 'expected_value'.
    """
    return 'foo'
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
Given the TestInfra host with URL "docker://java11" is ready
```

To connect to a Docker container called sut but give it 60 seconds to become
ready, use the following:

```gherkin
Given the TestInfra host with URL "docker://sut" is ready within 60 seconds
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
    Given the TestInfra host with URL "docker://sut" is ready within 10 seconds
    When the TestInfra system property type is not Windoze skip tests
```

## Upgrading from 2.Y.Z to 3.0.0

We introduced a number of breaking changes, namely:
- A change to the Domain Specific Language (DSL).
- Moving to TestInfra 9 and dropping support for 6, 7 and 8.
- Dropping support for EOL versions of Python (3.6, 3.7 and 3.8).

The changes for the DSL are pretty basic.  We identified a need to namespace
the TestInfra tests to stop clashes with other BDD feature code.  If your
old code looked something like:

```gherkin
  Scenario: System Package
    Given the host with URL "docker://sut" is ready
    When the package is ntp
    Then the package is installed
```

Then change the code to:

```gherkin
  Scenario: System Package
    Given the TestInfra host with URL "docker://sut" is ready
    When the TestInfra package is ntp
    Then the TestInfra package is installed
```

All example code above has been updated to the new format for guidance.

## Upgrading from 1.Y.Z to 2.0.0

We split the single package into multiple source files.  This means a minor
but nonetheless breaking change in your step definitions (all feature files
can remain as they are).  The change is how one sets `pytest_plugins`.

### Old Code

```python
pytest_plugins = ['testinfra_bdd']
```

### New Code

```python
pytest_plugins = testinfra_bdd.PYTEST_MODULES
```
