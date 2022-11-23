"""Then socket fixtures for testinfra-bdd."""
from pytest_bdd import (
    then,
    parsers,
    when
)


@when(parsers.parse('the socket is {socket}'))
def when_the_socket_is(socket, testinfra_bdd_host):
    """
    Check the status of a socket.

    Parameters
    ----------
    socket : str
        URL of the socket (e.g. "tpc://22").
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.
    """
    testinfra_bdd_host.socket = testinfra_bdd_host.host.socket(socket.strip('"'))


@then(parsers.parse('the socket is {expected_state}'))
def the_socket_is(expected_state, testinfra_bdd_host):
    """
    Check the state of a socket.

    Parameters
    ----------
    expected_state : str
        The expected state of the socket.
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        If the actual state does not match the state.
    """
    socket = testinfra_bdd_host.socket
    socket_url = testinfra_bdd_host.socket_url
    actual_state = 'not listening'
    assert socket, 'Socket is not set.  Have you missed a "When socket is" step?'

    if socket.is_listening:
        actual_state = 'listening'

    message = f'Expected socket {socket_url} to be {expected_state} but it is {actual_state}.'
    assert actual_state == expected_state, message
