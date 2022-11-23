"""Test exceptions are raised as expected."""
import pytest

from testinfra_bdd import get_host_fixture
from testinfra_bdd.address import when_the_address_and_port_is
from testinfra_bdd.command import the_command_is
from testinfra_bdd.pip import the_pip_package_is
from testinfra_bdd.pip import the_pip_package_state_is
from testinfra_bdd.process import the_process_filter_is


def test_invalid_command_stream_name():
    """Test that an exception is thrown when attempting to get an invalid resource type."""
    exception_raised = False

    try:
        host = get_host_fixture('docker://sut')
        the_command_is('ls', host)
        host.get_stream_from_command('foo')
    except ValueError as ex:
        exception_raised = True
        assert str(ex) == 'Unknown stream name "foo".'

    assert exception_raised, 'Expected an exception to be raised.'


def test_unready_host():
    """Test that a non-ready host throws an exception."""
    exception_raised = False

    try:
        get_host_fixture('docker://foo', 1)
    except AssertionError as ex:
        exception_raised = True
        assert str(ex) == 'The host docker://foo is not ready within 1 seconds.'

    assert exception_raised, 'Expected an exception to be raised.'


@pytest.mark.parametrize(
    'pip,expected_state,expected_exception_message',
    [
        (None, 'present', 'Pip package not set.  Have you missed a "When pip package is" step?'),
        ('semver', 'foo', 'Unknown expected state "foo" for a Pip package.'),
        ('semver', 'latest', 'Expected Pip package semver to be latest but it is superseded.')
    ]
)
def test_pip_package(pip, expected_state, expected_exception_message):
    """Test that a superseded pip package is identified."""
    exception_raised = False
    host = get_host_fixture('docker://sut')

    if pip:
        the_pip_package_is(pip, host)

    try:
        the_pip_package_state_is(expected_state, host)
    except (AssertionError, RuntimeError, ValueError) as ex:
        exception_raised = True
        assert str(ex) == expected_exception_message

    assert exception_raised, 'Expected an exception to be raised.'


@pytest.mark.parametrize(
    'process_specification',
    [
        '',
        'foo'
    ]
)
def test_invalid_process_specifications(process_specification):
    """Test that exceptions are raised when the process specification is invalid."""
    exception_raised = False
    expected_message = f'Unable to parse process filters "{process_specification}".'

    try:
        host = get_host_fixture('docker://sut')
        the_process_filter_is(process_specification, host)
    except ValueError as ex:
        exception_raised = True
        actual_message = str(ex)
        assert actual_message == expected_message

    assert exception_raised, 'Expected an exception to be raised.'


@pytest.mark.parametrize(
    'specification,exception_expected',
    [
        ('foo', True),
        ('foo:bar', True),
        ('localhost:0', False)
    ]
)
def test_invalid_addr_and_port_specifications(specification, exception_expected):
    """Test that exceptions are raised when the specification is invalid."""
    exception_raised = False
    expected_messages = {
        'foo': f'Unable to parse addr:port from "{specification}".',
        'foo:bar': f'Unable to parse addr:port from "{specification}". Unable to parse port.'
    }

    try:
        host = get_host_fixture('docker://sut')
        when_the_address_and_port_is(specification, host)
    except ValueError as ex:
        exception_raised = True
        actual_message = str(ex)
        assert actual_message == expected_messages[specification]

    if exception_expected:
        assert exception_raised, 'Expected an exception to be raised.'
