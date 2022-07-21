"""Then user fixtures for testinfra-bdd."""
from pytest_bdd import (
    then,
    parsers
)


@then(parsers.parse('the user {property_name} is {expected_value}'))
def the_user_property_is(property_name, expected_value, testinfra_bdd_host):
    """
    Check the property of a user.

    Parameters
    ----------
    property_name : str
        The name of the property to compare.
    expected_value : str
        The value that is expected.
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        If the actual value does not match the expected value.
    """
    user = testinfra_bdd_host.user
    assert user, 'User not set.  Have you missed a "When user is" step?'

    if testinfra_bdd_host.user.exists:
        actual_state = 'present'
        properties = {
            'gid': str(user.gid),
            'group': user.group,
            'home': user.home,
            'shell': user.shell,
            'state': actual_state,
            'uid': str(user.uid)
        }
    else:
        actual_state = 'absent'
        properties = {
            'state': actual_state
        }

    assert property_name in properties, f'Unknown user property "{property_name}".'
    actual_value = properties[property_name]
    message = f'Expected {property_name} for user {user.name} to be "{expected_value}" '
    message += f'but it was "{actual_value}".'
    assert actual_value == expected_value, message


@then(parsers.parse('the user is {expected_state}'))
def check_the_user_state(expected_state, testinfra_bdd_host):
    """
    Check that the actual state of a user matches the expected state.

    Parameters
    ----------
    expected_state : str
        The expected state (e.g. absent or present).
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.
    """
    the_user_property_is('state', expected_state, testinfra_bdd_host)
