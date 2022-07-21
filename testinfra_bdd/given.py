"""The given steps of testinfra-bdd."""
import testinfra_bdd.fixture
from pytest_bdd import given
from pytest_bdd import parsers


@given(parsers.parse('the host with URL "{hostspec}" is ready'), target_fixture='testinfra_bdd_host')
def the_host_is_ready(hostspec):
    """
    Ensure that the host is ready within the specified number of seconds.

    If the host does not become ready within the specified number of seconds,
    fail the tests.

    Parameters
    ----------
    hostspec : str
        The URL of the System Under Test (SUT).  Must comply to the Testinfra
        URL patterns.  See
        https://testinfra.readthedocs.io/en/latest/backends.html

    Returns
    -------
    testinfra_bdd.fixture.TestinfraBDD
        The object to return as a fixture.
    """
    return testinfra_bdd.get_host_fixture(hostspec)


@given(parsers.parse('the host with URL "{hostspec}" is ready within {seconds:d} seconds'),
       target_fixture='testinfra_bdd_host')
def the_host_is_ready_with_a_number_of_seconds(hostspec, seconds):
    """
    Ensure that the host is ready within the specified number of seconds.

    If the host does not become ready within the specified number of seconds,
    fail the tests.

    Parameters
    ----------
    hostspec : str
        The URL of the System Under Test (SUT).  Must comply to the Testinfra
        URL patterns.  See
        https://testinfra.readthedocs.io/en/latest/backends.html
    seconds : int
        The number of seconds that the host is expected to become ready in.

    Returns
    -------
    testinfra_bdd.fixture.TestinfraBDD
        The object to return as a fixture.
    """
    return testinfra_bdd.get_host_fixture(hostspec, seconds)
