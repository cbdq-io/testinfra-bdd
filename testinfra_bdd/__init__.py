"""
An interface between pytest-bdd and pytest-testinfra.

For documentation and examples, please go to
https://github.com/locp/testinfra-bdd

Please avoid already-imported warning: PYTEST_DONT_REWRITE.
"""
from testinfra_bdd.fixture import TestinfraBDD

"""PYTEST_MODULES.

A list of all testinfra-bdd packages that contain fixtures.
"""
PYTEST_MODULES = [
    'testinfra_bdd',
    'testinfra_bdd.given',
    'testinfra_bdd.then.address',
    'testinfra_bdd.then.command',
    'testinfra_bdd.then.file',
    'testinfra_bdd.then.group',
    'testinfra_bdd.then.package',
    'testinfra_bdd.then.pip',
    'testinfra_bdd.then.process',
    'testinfra_bdd.then.service',
    'testinfra_bdd.then.socket',
    'testinfra_bdd.then.user',
    'testinfra_bdd.when'
]

"""The version of the module.

This is used by setuptools and by gitchangelog to identify the name of the name
of the release.
"""
__version__ = '2.2.1'


def get_host_fixture(hostspec, timeout=0):
    """
    Return a host that is confirmed as ready.

    hostspec : str
        The URL of the System Under Test (SUT).  Must comply to the Testinfra
        URL patterns.  See
        https://testinfra.readthedocs.io/en/latest/backends.html
    timeout : int, optional
        The number of seconds that the host is expected to become ready in.

    Returns
    -------
    testinfra_bdd.fixture.TestinfraBDD
        The object to return as a fixture.

    Raises
    ------
    AssertError
        When the host is not ready.
    """
    if timeout:
        message = f'The host {hostspec} is not ready within {timeout} seconds.'
    else:
        message = f'The host {hostspec} is not ready.'

    host = TestinfraBDD(hostspec)
    assert host.is_host_ready(timeout), message
    return host
