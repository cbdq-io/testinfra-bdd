"""
An interface between pytest-bdd and pytest-testinfra.

For documentation and examples, please go to
https://github.com/locp/testinfra-bdd
"""
import re
import pytest

import testinfra_bdd.file
import testinfra_bdd.fixture
import testinfra_bdd.pip

from pytest_bdd import (
    given,
    when,
    then,
    parsers
)

"""The version of the module.

This is used by setuptools and by gitchangelog to identify the name of the name
of the release.
"""
__version__ = '1.0.6'


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
    return testinfra_bdd.fixture.get_host_fixture(hostspec)


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
    return testinfra_bdd.fixture.get_host_fixture(hostspec, seconds)


@when(parsers.parse('the {resource_type} is {resource_name}'))
@when(parsers.parse('the {resource_type} is "{resource_name}"'))
def the_resource_type_is(resource_type, resource_name, testinfra_bdd_host):
    """
    Get a resource of a specified type from the system under test.

    Parameters
    ----------
    resource_type : str
        The type of the resource.
    resource_name : str
        The name of the resource.
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.
    """
    testinfra_bdd_host.get_resource_from_host(resource_type, resource_name)


@when(parsers.parse('the system property {property_name} is not "{expected_value}" skip tests'))
@when(parsers.parse('the system property {property_name} is not {expected_value} skip tests'))
def skip_tests_if_system_info_does_not_match(property_name, expected_value, testinfra_bdd_host):
    """
    Skip tests if a system property does not patch the expected value.

    Parameters
    ----------
    property_name : str
    expected_value : str
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.
    """
    actual_value = testinfra_bdd_host.get_host_property(property_name)
    if actual_value != expected_value:
        pytest.skip(f'System {property_name} is {actual_value} which is not {expected_value}.')


#############################################################################
# Command checks.
#############################################################################
@then(parsers.parse('the command {command} exists in path'))
@then(parsers.parse('the command "{command}" exists in path'))
def check_command_exists_in_path(command, testinfra_bdd_host):
    """
    Assert that a specified command is present on the host path.

    Parameters
    ----------
    command : str
        The name of the command to check for.
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        When the command is not found on the path.
    """
    message = f'Unable to find the command "{command}" on the path.'
    assert testinfra_bdd_host.host.exists(command), message


@then(parsers.parse('the command {stream_name} contains "{text}"'))
def check_command_stream_contains(stream_name, text, testinfra_bdd_host):
    """
    Check that the stdout or stderr stream contains a string.

    Parameters
    ----------
    stream_name : str
        The name of the stream to check.  Must be "stdout" or "stderr".
    text : str
        The text to search for.
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        When the specified stream does not contain the expected text.
    """
    stream = testinfra_bdd_host.get_stream_from_command(stream_name)
    message = f'The string "{text}" was not found in the {stream_name} ("{stream}") of the command.'
    assert text in stream, message


@then(parsers.parse('the command {stream_name} contains the regex "{pattern}"'))
def check_command_stream_contains_the_regex(stream_name, pattern, testinfra_bdd_host):
    """
    Check that the stdout or stderr stream matches a regular expression pattern.

    Parameters
    ----------
    stream_name : str
        The name of the stream to be checked.  Must be stdout or stderr.
    pattern : str
        The pattern to search for in the stream.
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        When the specified stream does not match the pattern.
    ValueError
        When the stream name is not recognized.
    """
    stream = testinfra_bdd_host.get_stream_from_command(stream_name)
    message = f'The regex "{pattern}" is not found in the {stream_name} "{stream}".'
    # The parsers.parse function escapes the parsed string.  We need to clean it up before using it.
    pattern = pattern.encode('utf-8').decode('unicode_escape')
    prog = re.compile(pattern)
    assert prog.search(stream) is not None, message


@then(parsers.parse('the command return code is {expected_return_code:d}'))
def check_command_return_code(expected_return_code, testinfra_bdd_host):
    """
    Check that the expected return code from a command matches the actual return code.

    Parameters
    ----------
    expected_return_code : int
        The expected return code (e.g. zero/0).
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        When the actual return code does not match the expected return code.
    """
    cmd = testinfra_bdd_host.command
    actual_return_code = cmd.rc
    message = f'Expected a return code of {expected_return_code} but got {actual_return_code}.'
    assert expected_return_code == actual_return_code, message


@then(parsers.parse('the command {stream_name} is empty'))
def command_stream_is_empty(stream_name, testinfra_bdd_host):
    """
    Check that the specified command stream is empty.

    Parameters
    ----------
    stream_name : str
        The name of the stream to be checked.  Must be stdout or stderr.
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        When the specified stream does not match the pattern.
    """
    stream = testinfra_bdd_host.get_stream_from_command(stream_name)
    assert not stream, f'Expected {stream_name} to be empty ("{stream}").'


#############################################################################
# Service checks.
#############################################################################
@then('the service is not enabled')
def the_service_is_not_enabled(testinfra_bdd_host):
    """
    Check that the service is not enabled.

    Parameters
    ----------
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        When the service is enabled.
    """
    service = testinfra_bdd_host.service
    message = f'Expected {service.name} on host {testinfra_bdd_host.hostname} to be disabled, but it is enabled.'
    assert not service.is_enabled, message


@then('the service is enabled')
def the_service_is_enabled(testinfra_bdd_host):
    """
    Check that the service is enabled.

    Parameters
    ----------
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        When the service is not enabled.
    """
    service = testinfra_bdd_host.service
    message = f'Expected {service.name} on host {testinfra_bdd_host.hostname} to be enabled, but it is disabled.'
    assert service.is_enabled, message


@then('the service is not running')
def the_service_is_not_running(testinfra_bdd_host):
    """
    Check that the service is not running.

    Parameters
    ----------
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        When the service is running.
    """
    service = testinfra_bdd_host.service
    message = f'Expected {service.name} on host {testinfra_bdd_host.hostname} to not be running.'
    assert not service.is_running, message


@then('the service is running')
def the_service_is_running(testinfra_bdd_host):
    """
    Check that the service is running.

    Parameters
    ----------
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        When the service is not running.
    """
    service = testinfra_bdd_host.service
    message = f'Expected {service.name} on host {testinfra_bdd_host.hostname} to be running.'
    assert service.is_running, message


#############################################################################
#  Pip package checks.
#############################################################################
@then('the pip check is OK')
def the_pip_check_is_ok(testinfra_bdd_host):
    """
    Verify installed packages have compatible dependencies.

    Parameters
    ----------
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        When the packages have incompatible dependencies.
    """
    host = testinfra_bdd_host.host
    cmd = host.pip.check()
    message = f'Incompatible Pip packages - {cmd.stdout} {cmd.stderr}'
    assert cmd.rc == 0, message


@then(parsers.parse('the pip package state is {expected_state}'))
@then(parsers.parse('the pip package is {expected_state}'))
def the_pip_package_state_is(expected_state, testinfra_bdd_host):
    """
    Check the state of a Pip package.

    Parameters
    ----------
    expected_state : str
        The expected state of the package.  Can be absent, latest or installed.
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        When the actual state doesn't match the expected state.
    """
    (actual_state, message) = testinfra_bdd.pip.get_pip_package_actual_state(
        testinfra_bdd_host.pip_package,
        expected_state,
        testinfra_bdd_host.host
    )
    assert actual_state == expected_state, message


@then(parsers.parse('the pip package version is {expected_version}'))
def the_pip_package_version_is(expected_version, testinfra_bdd_host):
    """
    Check the version of a Pip package.

    Parameters
    ----------
    expected_version : str
        The version of the package that is expected.
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        When the actual version is not the expected version.
    """
    pip_package = testinfra_bdd_host.pip_package
    assert pip_package, 'Pip package not set.  Have you missed a "When pip package is" step?'
    actual_version = pip_package.version
    message = f'Expected Pip package version to be {expected_version} but it was {actual_version}.'
    assert actual_version == expected_version, message


#############################################################################
#  System package checks.
#############################################################################
@then(parsers.parse('the package state is {expected_status}'))
@then(parsers.parse('the package is {expected_status}'))
def the_package_status_is(expected_status, testinfra_bdd_host):
    """
    Check the status of a package (installed/absent).

    Parameters
    ----------
    expected_status : str
        Can be absent, installed or present.
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        When the package is not in the expected state.
    """
    status_lookup = {
        'absent': False,
        'installed': True,
        'present': True
    }
    expected_to_be_installed = status_lookup[expected_status]
    pkg = testinfra_bdd_host.package
    actual_status = pkg.is_installed

    if expected_to_be_installed:
        message = f'Expected {pkg.name} to be {expected_status} on {testinfra_bdd_host.hostname} but it is absent.'

    if actual_status:
        message = f'Expected {pkg.name} to be absent on {testinfra_bdd_host.hostname} '
        message += 'but it is installed ({pkg.version}).'

    assert actual_status == expected_to_be_installed, message


#############################################################################
#  File checks.
#############################################################################
@then(parsers.parse('the file contents contains "{text}"'))
def the_file_contents_contains_text(text, testinfra_bdd_host):
    """
    Check if the file contains a string.

    Parameters
    ----------
    text : str
        The string to search for in the file content.
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        When the file does not contain the string.
    """
    file = testinfra_bdd_host.file
    assert file.contains(text), f'The file {testinfra_bdd_host.hostname}:{file.path} does not contain "{text}".'


@then(parsers.parse('the file contents contains the regex "{pattern}"'))
def the_file_contents_matches_the_regex(pattern, testinfra_bdd_host):
    """
    Check if the file contains matches a regex pattern.

    Parameters
    ----------
    pattern : str
        The regular expression to match against the file content.
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        When the regex does not match the file content.
    """
    file = testinfra_bdd_host.file
    file_name = f'{testinfra_bdd_host.hostname}:{file.path}'
    message = f'The regex "{pattern}" does not match the content of {file_name} ("{file.content_string}").'
    # The parsers.parse function escapes the parsed string.  We need to clean it up before using it.
    pattern = pattern.encode('utf-8').decode('unicode_escape')
    assert re.search(pattern, file.content_string) is not None, message


@then(parsers.parse('the file is {expected_status}'))
def the_file_status(expected_status, testinfra_bdd_host):
    """
    Check if the file is present or absent.

    Parameters
    ----------
    expected_status : str
        Should be present or absent.
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        When the expected status does not match the actual status.
    """
    the_file_property_is('state', expected_status, testinfra_bdd_host)


@then(parsers.parse('the file {property_name} is {expected_value}'))
def the_file_property_is(property_name, expected_value, testinfra_bdd_host):
    """
    Check the property of a file.

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
    (actual_value, exception_message) = testinfra_bdd.file.get_file_actual_state(
        testinfra_bdd_host.file,
        property_name,
        expected_value
    )
    assert actual_value == expected_value, exception_message


#############################################################################
#  User checks.
#############################################################################
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


#############################################################################
#  Group checks.
#############################################################################
@then(parsers.parse('the group {property_name} is {expected_value}'))
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


@then(parsers.parse('the group is {expected_state}'))
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


#############################################################################
#  Process checks.
#############################################################################
@then(parsers.parse('the process count is {expected_count:d}'))
def the_process_count_is(expected_count, testinfra_bdd_host):
    """
    Check that the process count matches the expected count.

    Parameters
    ----------
    expected_count : int
        The expected number of processes.
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        If the actual process count does not match the expected count.
    """
    specification = testinfra_bdd_host.process_specification
    processes = testinfra_bdd_host.processes
    assert processes, 'No process set, did you forget a "When process filter" step?'
    actual_process_count = len(processes)
    message = f'Expected process specification "{specification}" to return {expected_count} '
    message += f'but found {actual_process_count} "{processes}".'
    assert actual_process_count == expected_count, message


#############################################################################
#  Process checks.
#############################################################################
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


#############################################################################
#  Socket checks.
#############################################################################
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
