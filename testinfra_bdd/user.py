"""Then user fixtures for testinfra-bdd."""
from pytest_bdd import parsers, then, when


@when(parsers.parse('the TestInfra user is {username}'))
def the_user_is(username: str, testinfra_bdd_host):
    """
    Check the status of a user.

    Parameters
    ----------
    username : str
        The user name (e.g. "ben").
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.
    """
    testinfra_bdd_host.user = testinfra_bdd_host.host.user(username.strip('"'))


@then(parsers.parse('the TestInfra user {property_name} is {expected_value}'))
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


@then(parsers.parse('the TestInfra user is {expected_state}'))
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


@then(parsers.parse('the TestInfra user groups include "{expected_group}"'))
def check_the_user_included_groups(expected_group: str, testinfra_bdd_host: object):
    """
    Check that the user is a member of the specified group.

    Parameters
    ----------
    expected_group : str
        The group to check the user is a member of.
    testinfra_bdd_host : object
        The test fixture.

    Raises
    ------
    AssertError
        If the group doesn't exist or the user is not a member of the group.
    """
    user = testinfra_bdd_host.user
    assert user, 'User not set.  Have you missed a "When user is" step?'
    group = testinfra_bdd_host.host.group(expected_group)
    message = f'Expected group "{expected_group}" to exist.'
    assert group.exists, message
    message = f'Expected user "{user}" to be a member of group "{group.name}".'
    assert user.name in group.members, message
