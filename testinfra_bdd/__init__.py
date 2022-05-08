"""
An interface between pytest-bdd and pytest-testinfra.

For documentation and examples, please go to
https://github.com/locp/testinfra-bdd
"""
import re

import pytest
import testinfra

from pytest_bdd import (
    given,
    when,
    then,
    parsers
)

from testinfra_bdd.utils import (
    get_host_from_fixture,
    get_host_property,
    get_resource_from_fixture,
    get_resource_from_host,
    get_stream_from_command,
    is_host_ready
)

"""The version of the module.

This is used by setuptools and by gitchangelog to identify the name of the name
of the release.
"""
__version__ = '0.1.0'


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

    Raises
    ------
    AssertError
        If the host is not ready.
    """
    host = testinfra.get_host(hostspec)

    message = f'The host {hostspec} is not ready.'
    assert is_host_ready(host), message
    return {
        'host': host,
        'url': hostspec
    }


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

    Raises
    ------
    AssertError
        If the host does not become ready within the specified number of seconds.
    """
    host = testinfra.get_host(hostspec)

    message = f'The host {hostspec} is not ready within {seconds} seconds.'
    assert is_host_ready(host, seconds), message
    return {
        'host': host,
        'url': hostspec
    }


@when(parsers.parse('the {resource_type} is "{resource_name}"'))
@when(parsers.parse('the {resource_type} is {resource_name}'))
def the_resource_type_is(resource_type, resource_name, testinfra_bdd_host):
    """
    Get a resource of a specified type from the system under test.

    Parameters
    ----------
    resource_type : str
        The type of the resource.
    resource_name : str
        The name of the resource.
    testinfra_bdd_host : dict
        The test fixture.
    """
    host = get_host_from_fixture(testinfra_bdd_host)
    testinfra_bdd_host[resource_type] = get_resource_from_host(host, resource_type, resource_name)


@when(parsers.parse('the system property {property_name} is not "{expected_value}" skip tests'))
@when(parsers.parse('the system property {property_name} is not {expected_value} skip tests'))
def skip_tests_if_system_info_does_not_match(property_name, expected_value, testinfra_bdd_host):
    """
    Skip tests if a system property does not patch the expected value.

    Parameters
    ----------
    property_name : str
    expected_value : str
    testinfra_bdd_host : dict
        The test fixture.
    """
    host = get_host_from_fixture(testinfra_bdd_host)
    actual_value = get_host_property(host, property_name)

    if actual_value != expected_value:
        pytest.skip(f'System {property_name} is {actual_value} which is not {expected_value}.')


@then(parsers.parse('the command "{command}" exists in path'))
@then(parsers.parse('the command {command} exists in path'))
def check_command_exists_in_path(command, testinfra_bdd_host):
    """
    Assert that a specified command is present on the host path.

    Parameters
    ----------
    command : str
        The name of the command to check for.
    testinfra_bdd_host : dict
        The test fixture.

    Raises
    ------
    AssertError
        When the command is not found on the path.
    """
    host = get_host_from_fixture(testinfra_bdd_host)
    message = f'Unable to find the command "{command}" on the path.'
    assert host.exists(command), message


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
    testinfra_bdd_host : dict
        The test fixture.

    Raises
    ------
    AssertError
        When the specified stream does not contain the expected text.
    """
    cmd = get_resource_from_fixture(testinfra_bdd_host, 'command')
    stream = get_stream_from_command(cmd, stream_name)
    message = f'The string "{text}" was not found in the {stream_name} ("{stream}") of the command.'
    assert text in stream, message


@then(parsers.parse('the command {stream_name} matches regex "{pattern}"'))
def check_command_stream_matches_regex(stream_name, pattern, testinfra_bdd_host):
    """
    Check that the stdout or stderr stream matches a regular expression pattern.

    Parameters
    ----------
    stream_name : str
        The name of the stream to be checked.  Must be stdout or stderr.
    pattern : str
        The pattern to search for in the stream.
    testinfra_bdd_host : dict
        The test fixture.

    Raises
    ------
    AssertError
        When the specified stream does not match the pattern.
    ValueError
        When the stream name is not recognized.
    """
    cmd = get_resource_from_fixture(testinfra_bdd_host, 'command')
    stream = get_stream_from_command(cmd, stream_name)
    message = f'The regex "{pattern}" does not match the {stream_name} "{stream}".'
    # The parsers.parse function escapes the parsed string.  We need to clean it up before using it.
    pattern = pattern.encode('utf-8').decode('unicode_escape')
    prog = re.compile(pattern)
    assert prog.match(stream) is not None, message


@then(parsers.parse('the command return code is {expected_return_code:d}'))
def check_command_return_code(expected_return_code, testinfra_bdd_host):
    """
    Check that the expected return code from a command matches the actual return code.

    Parameters
    ----------
    expected_return_code : int
        The expected return code (e.g. zero/0).
    testinfra_bdd_host : dict
        The test fixture.

    Raises
    ------
    AssertError
        When the actual return code does not match the expected return code.
    """
    cmd = get_resource_from_fixture(testinfra_bdd_host, 'command')
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
    testinfra_bdd_host : dict
        The test fixture.

    Raises
    ------
    AssertError
        When the specified stream does not match the pattern.
    """
    cmd = get_resource_from_fixture(testinfra_bdd_host, 'command')
    stream = get_stream_from_command(cmd, stream_name)
    assert not stream, f'Expected {stream_name} to be empty ("{stream}").'


@then('the service is not enabled')
def the_service_is_not_enabled(testinfra_bdd_host):
    """
    Check that the service is not enabled.

    Parameters
    ----------
    testinfra_bdd_host : dict
        The test fixture.

    Raises
    ------
    AssertError
        When the service is enabled.
    """
    service = get_resource_from_fixture(testinfra_bdd_host, 'service')
    host = get_host_from_fixture(testinfra_bdd_host)
    message = f'Expected {service.name} on host {host.backend.hostname} to be disabled, but it is enabled.'
    assert not service.is_enabled, message


@then('the service is enabled')
def the_service_is_enabled(testinfra_bdd_host):
    """
    Check that the service is enabled.

    Parameters
    ----------
    testinfra_bdd_host : dict
        The test fixture.

    Raises
    ------
    AssertError
        When the service is not enabled.
    """
    service = get_resource_from_fixture(testinfra_bdd_host, 'service')
    host = get_host_from_fixture(testinfra_bdd_host)
    message = f'Expected {service.name} on host {host.backend.hostname} to be enabled, but it is disabled.'
    assert service.is_enabled, message


@then('the service is not running')
def the_service_is_not_running(testinfra_bdd_host):
    """
    Check that the service is not running.

    Parameters
    ----------
    testinfra_bdd_host : dict
        The test fixture.

    Raises
    ------
    AssertError
        When the service is running.
    """
    service = get_resource_from_fixture(testinfra_bdd_host, 'service')
    host = get_host_from_fixture(testinfra_bdd_host)
    message = f'Expected {service.name} on host {host.backend.hostname} to not be running.'
    assert not service.is_running, message


@then('the service is running')
def the_service_is_running(testinfra_bdd_host):
    """
    Check that the service is running.

    Parameters
    ----------
    testinfra_bdd_host : dict
        The test fixture.

    Raises
    ------
    AssertError
        When the service is not running.
    """
    service = get_resource_from_fixture(testinfra_bdd_host, 'service')
    host = get_host_from_fixture(testinfra_bdd_host)
    message = f'Expected {service.name} on host {host.backend.hostname} to be running.'
    assert service.is_running, message


@then(parsers.parse('the package is {expected_status}'))
def the_package_status_is(expected_status, testinfra_bdd_host):
    """
    Check the status of a package (installed/absent).

    Parameters
    ----------
    expected_status : str
        Can be absent, installed or present.
    testinfra_bdd_host : dict
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
    pkg = get_resource_from_fixture(testinfra_bdd_host, 'package')
    host = get_host_from_fixture(testinfra_bdd_host)
    actual_status = pkg.is_installed

    if expected_to_be_installed:
        message = f'Expected {pkg.name} to be {expected_status} on {host.backend.hostname} but it is absent.'

    if actual_status:
        message = f'Expected {pkg.name} to be absent on {host.backend.hostname} but it is installed ({pkg.version}).'

    assert actual_status == expected_to_be_installed, message


@then(parsers.parse('the file contents contains "{text}"'))
def the_file_contents_contains_text(text, testinfra_bdd_host):
    """
    Check if the file contains a string.

    Parameters
    ----------
    text : str
        The string to search for in the file content.
    testinfra_bdd_host : dict
        The test fixture.

    Raises
    ------
    AssertError
        When the file does not contain the string.
    """
    file = get_resource_from_fixture(testinfra_bdd_host, 'file')
    host = get_host_from_fixture(testinfra_bdd_host)
    assert file.contains(text), f'The file {host.backend.hostname}:{file.path} does not contain "{text}".'


@then(parsers.parse('the file contents contains the regex "{pattern}"'))
def the_file_contents_matches_the_regex(pattern, testinfra_bdd_host):
    """
    Check if the file contains matches a regex pattern.

    Parameters
    ----------
    pattern : str
        The regular expression to match against the file content.
    testinfra_bdd_host : dict
        The test fixture.

    Raises
    ------
    AssertError
        When the regex does not match the file content.
    """
    file = get_resource_from_fixture(testinfra_bdd_host, 'file')
    host = get_host_from_fixture(testinfra_bdd_host)
    file_name = f'{host.backend.hostname}:{file.path}'
    message = f'The regex "{pattern}" does not match the content of {file_name} ("{file.content_string}").'
    # The parsers.parse function escapes the parsed string.  We need to clean it up before using it.
    pattern = pattern.encode('utf-8').decode('unicode_escape')
    assert re.search(pattern, file.content_string) is not None, message


@then(parsers.parse('the file group is {expected_group_name}'))
def the_file_group_is_ntp(expected_group_name, testinfra_bdd_host):
    """
    Check if the file group name is as expected.

    Parameters
    ----------
    expected_group_name : str
        The name one expects the group name to match.
    testinfra_bdd_host : dict
        The test fixture.

    Raises
    ------
    AssertError
        When the expected group name does not match the actual group name.
    """
    file = get_resource_from_fixture(testinfra_bdd_host, 'file')
    host = get_host_from_fixture(testinfra_bdd_host)
    actual_group_name = file.group
    message = f'Expected the group name for {host.backend.hostname}:{file.path} to be {expected_group_name} '
    message += f'but it is {actual_group_name}.'
    assert expected_group_name == actual_group_name, message


@then(parsers.parse('the file is {expected_status}'))
def the_file_status(expected_status, testinfra_bdd_host):
    """
    Check if the file is present or absent.

    Parameters
    ----------
    expected_status : str
        Should be present or absent.
    testinfra_bdd_host : dict
        The test fixture.

    Raises
    ------
    AssertError
        When the expected status does not match the actual status.
    """
    status_lookup = {
        'absent': False,
        'present': True
    }
    is_expected_to_exist = status_lookup[expected_status]
    host = get_host_from_fixture(testinfra_bdd_host)
    file = get_resource_from_fixture(testinfra_bdd_host, 'file')

    if is_expected_to_exist:
        message = f'The file {file.path} is expected to exist on {host.backend.hostname} but is absent.'
    else:
        message = f'The file {file.path} is expected to be absent on {host.backend.hostname} but is present.'

    assert is_expected_to_exist == file.exists, message


@then(parsers.parse('the file mode is {expected_file_mode}'))
def the_file_mode_is_0o544(expected_file_mode, testinfra_bdd_host):
    """
    Check that the expected file mode matches the actual file mode.

    Parameters
    ----------
    expected_file_mode : str
        Must be an octal string representing the expected file mode.
    testinfra_bdd_host : dict
        The test fixture.

    Raises
    ------
    AssertError
        When the expected mode does not match the actual mode.
    """
    file = get_resource_from_fixture(testinfra_bdd_host, 'file')
    actual_file_mode = '0o%o' % file.mode
    host = get_host_from_fixture(testinfra_bdd_host)
    message = f'Expected the mode for {host.backend.hostname}:{file.path} to be {expected_file_mode} '
    message += f'not {actual_file_mode}.'
    assert expected_file_mode == actual_file_mode, message


@then(parsers.parse('the file owner is {expected_username}'))
def the_file_owner_is_ntp(expected_username, testinfra_bdd_host):
    """
    Check the expected username of the owner matches the actual username.

    Parameters
    ----------
    expected_username : str
        The expected username.
    testinfra_bdd_host : dict
        The test fixture.

    Raises
    ------
    AssertError
        When the expected username does not match the actual username.
    """
    file = get_resource_from_fixture(testinfra_bdd_host, 'file')
    host = get_host_from_fixture(testinfra_bdd_host)
    actual_username = file.user
    message = f'Expected {host.backend.hostname}:{file.path} to be owned by {expected_username}, '
    message += f'not by {actual_username}.'
    assert expected_username == actual_username, message


@then(parsers.parse('the file type is {expected_file_type}'))
def the_file_type_is_file(expected_file_type, testinfra_bdd_host):
    """
    Check that the expected file type matches the actual file type.

    Parameters
    ----------
    expected_file_type : str
        The expected file type.  Can be one of file, directory, pipe, socket or symlink.
    testinfra_bdd_host : dict
        The test fixture.

    Raises
    ------
    AssertError
        When the expected file type does not match the actual file type.
    """
    file = get_resource_from_fixture(testinfra_bdd_host, 'file')
    host = get_host_from_fixture(testinfra_bdd_host)
    type_lookup = {
        'file': file.is_file,
        'directory': file.is_directory,
        'pipe': file.is_pipe,
        'socket': file.is_socket,
        'symlink': file.is_symlink
    }
    message = f'file {file.path} on {host.backend.hostname} is not a {expected_file_type}.'
    assert type_lookup[expected_file_type], message
