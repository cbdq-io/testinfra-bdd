"""Then file fixtures for testinfra-bdd."""
from pytest_bdd import parsers, then, when


@when(parsers.parse('the TestInfra group is {groupname}'))
def the_group_is(groupname: str, testinfra_bdd_host):
    """
    Check the status of a group.

    Parameters
    ----------
    groupname : str
        The group name (e.g. "admin").
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.
    """
    testinfra_bdd_host.group = testinfra_bdd_host.host.group(groupname.strip('"'))


@then(parsers.parse('the TestInfra group contains the user "{expected_user}"'))
def _(expected_user: str, testinfra_bdd_host):
    """
    Check that the expected user is contained within a group.

    Parameters
    ----------
    expected_user : str
        _description_
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        If the group doesn't contain the expected user.
    """
    group = testinfra_bdd_host.group
    assert group, 'Group not set.  Have you missed a "When group is" step?'
    message = 'Expected group "{group.name}" to exist.'
    assert group.exists, message
    message = f'Expected the group "{group.name}" to contain the user "{expected_user}".'
    assert expected_user in group.members, message


@then(parsers.parse('the TestInfra group {property_name} is {expected_value}'))
def the_group_property_is(property_name, expected_value, testinfra_bdd_host):
    """
    Check the property of a group.

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
    group = testinfra_bdd_host.group
    assert group, 'Group not set.  Have you missed a "When group is" step?'

    properties = {
        'gid': None,
        'state': 'absent'
    }

    if group.exists:
        properties = {
            'gid': str(group.gid),
            'state': 'present'
        }

    assert property_name in properties, f'Unknown group property ({property_name}).'
    actual_value = properties[property_name]
    message = f'Expected group property to be {expected_value} but it was {actual_value}.'
    assert actual_value == expected_value, message


@then(parsers.parse('the TestInfra group is {expected_state}'))
def check_the_group_state(expected_state, testinfra_bdd_host):
    """
    Check that the actual state of a group matches the expected state.

    Parameters
    ----------
    expected_state : str
        The expected state (e.g. absent or present).
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.
    """
    the_group_property_is('state', expected_state, testinfra_bdd_host)
