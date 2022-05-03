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
