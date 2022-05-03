# testinfra-bdd

[![CI](https://github.com/locp/testinfra-bdd/actions/workflows/ci.yml/badge.svg)](https://github.com/locp/testinfra-bdd/actions/workflows/ci.yml)

An interface between pytest-bdd and pytest-testinfra.

## Defining a Scenario

Given a directory structure of:

```shell
(root) --+
         |
         |- tests +
                  |
                  +- features +
                  |           |
                  |           + example.feature
                  |
                  +- step_defs +
                               |
                               + test_example.py
```

The file `tests/features/example.feature` could look something like:

```gherkin
Feature: Example of Testinfra BDD
  Give an example of the possible Given, When and Then steps.

  Scenario: System Under Test
    Given Testinfra URL is docker://sut
    When Testinfra host is ready within 10 seconds
```

and `tests/step_defs/test_example.py` contains the following:

```python
from pytest_bdd import scenario

# Ensure that the PyTest fixtures provided in testinfra-bdd are available to
# your test suite.
pytest_plugins = ['testinfra_bdd']


@scenario('../features/example.feature', 'System Under Test')
def test_system_under_test():
    """System Under Test."""
```
## "Given" Steps

Given steps require that the URL of the system to be tested (SUT) is provided.
This URL should comply to the connection string for the [Testinfra connection
string](https://testinfra.readthedocs.io/en/latest/backends.html) (e.g.
docker://my-host).

Example:

To connect to a Docker container called sut:
```gherkin
Given Testinfra URL is docker://sut
```

### Writing a customized "Given" Step

It may be that you may want to create a customized "Given" step.  An example
could be that the hosts to be tested may be parametrized.  The "Given" step
must return a target fixture called "testinfra_bdd_host" so that the rest of
the Testinfra BDD fixtures will function.  An example of a parametrized
feature file can be seen at
[tests/features/parametrized.feature](tests/features/parametrized.feature)
and the
associated step definitions can be seen in
[tests/features/parametrized.feature](tests/features/parametrized.feature).

## "When" Steps

When steps require that a "Given" step has been executed beforehand.

Use the "When" steps to ascertain if the host is ready to have tests
executed against it or to ensure that the profile of the host being
tested matches expectations.  If they don't match, one can skip tests.

Whether a host is ready is ascertained by making a call to the SystemInfo
module of Testinfra to get the type (e.g. 'linux') of the system.  If this
fails for any reason, then it is assumed that the host is not ready.

### Check if the Host is Ready or Fail

In this example if the host is not ready, the tests will be marked
as failed:

```gherkin
When Testinfra host is ready
```

In this example if the host is not ready within 300 seconds (five minutes)
the tests will be marked as failed:

```gherkin
When Testinfra host is ready within 300 seconds
```

In this example, if the host is not ready, skip the tests:

```gherkin
When Testinfra host is ready or skip tests
```

In this example if the host is not ready within 300 seconds (five minutes)
skip the tests:

```gherkin
When Testinfra host is ready within 300 seconds or skip tests
```

### Skip Tests if Host Profile Does Not Match

It may be useful to skip tests if you find that the system under test doesn't
match an expected profile (e.g. the system is not debian as expected).  This
can be achieved by comparing against the following configurations:

- The OS Type (e.g. linux).
- The distribution name (e.g. debian).
- The OS release (e.g. 11).
- The OS codename if relevant (e.g. bullseye).
- The host architecture (e.g. x86_64).

Please note that to be able to get these values, the host must be ready.
This example shows all the possible combinations:

```gherkin
    When Testinfra host is ready within 10 seconds
    And Testinfra host type is linux or skip tests
    And Testinfra host distribution is debian or skip tests
    And Testinfra host release is 11 or skip tests
    And Testinfra host codename is bullseye or skip tests
    And Testinfra host arch is x86_64 or skip tests
```

If the host is anything other than Debian 11 (bullseye) running on x86_64
architecture, the tests will be skipped.
