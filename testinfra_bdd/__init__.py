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
