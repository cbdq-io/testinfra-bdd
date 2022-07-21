"""Then address fixtures for testinfra-bdd."""
from pytest_bdd import (
    then,
    parsers
)


@then(parsers.parse('the address is {expected_state}'))
def the_address_is(expected_state, testinfra_bdd_host):
    """
    Check the actual state of an address against an expected state.

    Parameters
    ----------
    expected_state : str
        The expected state of the address.

    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        If the actual state does not match the state.
    """
    address = testinfra_bdd_host.address
    assert address, 'Address is not set.  Did you miss a "When address is" step?'
    properties = {
        'resolvable': address.is_resolvable,
        'reachable': address.is_reachable
    }
    assert expected_state in properties, f'Invalid state for {address.name} ("{expected_state}").'
    message = f'Expected the address {address.name} to be {expected_state} but it is not.'
    assert properties[expected_state], message


@then(parsers.parse('the port is {expected_state}'))
def the_port_is(expected_state, testinfra_bdd_host):
    """
    Check the actual state of an address port against an expected state.

    Parameters
    ----------
    expected_state : str
        The expected state of the port.

    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        If the actual state does not match the state.
    """
    port = testinfra_bdd_host.port
    assert port, 'Port is not set.  Did you miss a "When the address and port" step?'
    properties = {
        'reachable': port.is_reachable
    }
    assert expected_state in properties, f'Unknown Port property ("{expected_state}").'
    message = f'{testinfra_bdd_host.address.name}:{testinfra_bdd_host.port_number} is unreachable.'
    assert properties['reachable'], message
