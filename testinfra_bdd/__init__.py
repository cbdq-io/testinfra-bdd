"""
An interface between pytest-bdd and pytest-testinfra.

For documentation and examples, please go to
https://github.com/locp/testinfra-bdd
"""
import re
import time

import pytest
import testinfra

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
__version__ = '0.2.3'


class TestinfraBDD:
    """A class that is used as the fixture in the given/when/then steps."""

    def __init__(self, url):
        """
        Create a TestinfraBDD object.

        Initialises the host attribute.

        Parameters
        ----------
        url : str
            The URL of the System Under Test (SUT).  Must comply to the Testinfra
            URL patterns.  See https://testinfra.readthedocs.io/en/latest/backends.html
        """
        self.arch = None
        self.codename = None
        self.command = None
        self.distribution = None
        self.file = None
        self.host = testinfra.get_host(url)
        self.hostname = None
        self.package = None
        self.release = None
        self.service = None
        self.type = None
        self.url = url
        self.user = None

    def get_host_property(self, property_name):
        """
        Get a named host property.

        Parameters
        ----------
        property_name : str
            The name of the property to be extracted.

        Raises
        ------
        AssertError
            If the property_name is invalid.

        Returns
        -------
        str
            The value of the property.
        """
        properties = {
            'type': self.host.system_info.type,
            'distribution': self.host.system_info.distribution,
            'release': self.host.system_info.release,
            'codename': self.host.system_info.codename,
            'arch': self.host.system_info.arch,
            'hostname': self.host.backend.get_hostname()
        }

        assert property_name in properties, f'Invalid host property name "{property_name}".'
        return properties[property_name]

    def get_resource_from_host(self, resource_type, resource_name):
        """
        Use a Testinfra module to get a resource from the system under test.

        Parameters
        ----------
        resource_type : str
            The type of resource to be examined.
        resource_name : str
            The name of the resource to be examined.  If resource_type is "command" then this is the
            command line to be executed.

        Returns
        -------
        object
            The resource that has been requested.
        """
        resource_type_is_set = True

        if resource_type == 'command':
            self.command = self.host.run(resource_name)
        elif resource_type == 'service':
            self.service = self.host.service(resource_name)
        elif resource_type == 'package':
            self.package = self.host.package(resource_name)
        elif resource_type == 'file':
            self.file = self.host.file(resource_name)
        elif resource_type == 'user':
            self.user = self.host.user(resource_name)
        else:
            resource_type_is_set = False

        assert resource_type_is_set, f'Unknown resource type "{resource_type}".'

    def get_stream_from_command(self, stream_name):
        """
        Get a named stream from the command.

        Parameters
        ----------
        stream_name : str
            The name of the stream.

        Raises
        ------
        AssertError
            If the command attribute is None.
        ValueError
            When the stream name is not recognized.

        Returns
        -------
        str
            The requested stream content.
        """
        assert self.command, 'No command has been executed.'

        if stream_name == 'stdout':
            return self.command.stdout
        elif stream_name == 'stderr':
            return self.command.stderr

        raise ValueError(f'Unknown stream name "{stream_name}".')

    def is_host_ready(self, timeout=0):
        """
        Check if a host is ready within a specified time.

        Will poll the host every second until timeout number of seconds have
        expired.  If this host has not responded within that time, the host
        is assumed to not be ready.

        Parameters
        ----------
        timeout : int,optional
            The time in seconds to wait for the host to become ready.  The
            default is zero.

        Returns
        -------
        bool
            True if the host is responding to the host.system_info.type request.
            False if it doesn't.
        """
        is_ready = False
        now = time.time()
        deadline = now + timeout

        while now <= deadline and not is_ready:
            try:
                self.host.system_info.type
                is_ready = True
                self.arch = self.host.system_info.arch
                self.codename = self.host.system_info.codename
                self.distribution = self.host.system_info.distribution
                self.hostname = self.host.backend.hostname
                self.release = self.host.system_info.release
                self.type = self.host.system_info.type
            except AssertionError:
                if now < deadline:
                    time.sleep(1)

            now = time.time()

        return is_ready


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
    host = TestinfraBDD(hostspec)

    message = f'The host {hostspec} is not ready.'
    assert host.is_host_ready(), message
    return host


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
    host = TestinfraBDD(hostspec)

    message = f'The host {hostspec} is not ready within {seconds} seconds.'
    assert host.is_host_ready(seconds), message
    return host


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
    testinfra_bdd_host : TestinfraBDD
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
    testinfra_bdd_host : TestinfraBDD
        The test fixture.
    """
    actual_value = testinfra_bdd_host.get_host_property(property_name)

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
    testinfra_bdd_host : TestinfraBDD
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
    testinfra_bdd_host : TestinfraBDD
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
    testinfra_bdd_host : TestinfraBDD
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
    testinfra_bdd_host : TestinfraBDD
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
    testinfra_bdd_host : TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        When the specified stream does not match the pattern.
    """
    stream = testinfra_bdd_host.get_stream_from_command(stream_name)
    assert not stream, f'Expected {stream_name} to be empty ("{stream}").'


@then('the service is not enabled')
def the_service_is_not_enabled(testinfra_bdd_host):
    """
    Check that the service is not enabled.

    Parameters
    ----------
    testinfra_bdd_host : TestinfraBDD
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
    testinfra_bdd_host : TestinfraBDD
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
    testinfra_bdd_host : TestinfraBDD
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
    testinfra_bdd_host : TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        When the service is not running.
    """
    service = testinfra_bdd_host.service
    message = f'Expected {service.name} on host {testinfra_bdd_host.hostname} to be running.'
    assert service.is_running, message


@then(parsers.parse('the package is {expected_status}'))
def the_package_status_is(expected_status, testinfra_bdd_host):
    """
    Check the status of a package (installed/absent).

    Parameters
    ----------
    expected_status : str
        Can be absent, installed or present.
    testinfra_bdd_host : TestinfraBDD
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


@then(parsers.parse('the file contents contains "{text}"'))
def the_file_contents_contains_text(text, testinfra_bdd_host):
    """
    Check if the file contains a string.

    Parameters
    ----------
    text : str
        The string to search for in the file content.
    testinfra_bdd_host : TestinfraBDD
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
    testinfra_bdd_host : TestinfraBDD
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
    testinfra_bdd_host : TestinfraBDD
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
    testinfra_bdd_host : TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        If the actual value does not match the expected value.
    """
    file = testinfra_bdd_host.file
    assert file, 'File not initialised.  Have you missed a "When file is" step?'
    actual_type = None

    if file.exists:
        actual_file_state = 'present'
        actual_file_mode = '0o%o' % file.mode
        type_lookup = {
            'file': file.is_file,
            'directory': file.is_directory,
            'pipe': file.is_pipe,
            'socket': file.is_socket,
            'symlink': file.is_symlink
        }

        for key in type_lookup.keys():
            if type_lookup[key]:
                actual_type = key
                break

        properties = {
            'group': file.group,
            'mode': actual_file_mode,
            'owner': file.user,
            'state': actual_file_state,
            'type': actual_type,
            'user': file.user
        }
    else:
        actual_file_state = 'absent'
        properties = {
            'state': actual_file_state,
            'type': None
        }

    assert property_name in properties, f'Unknown user property "{property_name}".'
    actual_value = properties[property_name]
    message = f'Expected {property_name} for file {file.path} to be "{expected_value}" '
    message += f'but it was "{actual_value}".'
    assert actual_value == expected_value, message


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
    testinfra_bdd_host : TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        If the actual value does not match the expected value.
    """
    user = testinfra_bdd_host.user
    assert user, 'User not initialised.  Have you missed a "When user is" step?'

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
