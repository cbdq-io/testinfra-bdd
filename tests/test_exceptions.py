"""Test exceptions are raised as expected."""
import pytest
import testinfra_bdd
import testinfra_bdd.fixture


def test_invalid_resource_type():
    """Test that an exception is thrown when attempting to get an invalid resource type."""
    exception_raised = False

    try:
        host = testinfra_bdd.fixture.get_host_fixture('docker://sut')
        host.get_resource_from_host('foo', 'foo')
    except ValueError as ex:
        exception_raised = True
        assert str(ex) == 'Unknown resource type "foo".'

    assert exception_raised, 'Expected an exception to be raised.'


def test_invalid_command_stream_name():
    """Test that an exception is thrown when attempting to get an invalid resource type."""
    exception_raised = False

    try:
        host = testinfra_bdd.fixture.get_host_fixture('docker://sut')
        host.get_resource_from_host('command', 'ls')
        host.get_stream_from_command('foo')
    except ValueError as ex:
        exception_raised = True
        assert str(ex) == 'Unknown stream name "foo".'

    assert exception_raised, 'Expected an exception to be raised.'


def test_unready_host():
    """Test that a non-ready host throws an exception."""
    exception_raised = False

    try:
        testinfra_bdd.fixture.get_host_fixture('docker://foo', 1)
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
    host = testinfra_bdd.fixture.get_host_fixture('docker://sut')

    if pip:
        host.get_resource_from_host('pip package', pip)

    try:
        testinfra_bdd.the_pip_package_state_is(expected_state, host)
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
        host = testinfra_bdd.fixture.get_host_fixture('docker://sut')
        host.get_resource_from_host('process filter', process_specification)
    except ValueError as ex:
        exception_raised = True
        actual_message = str(ex)
        assert actual_message == expected_message

    assert exception_raised, 'Expected an exception to be raised.'


@pytest.mark.parametrize(
    'specification',
    [
        'foo',
        'foo:bar'
    ]
)
def test_invalid_addr_and_port_specifications(specification):
    """Test that exceptions are raised when the specification is invalid."""
    exception_raised = False
    expected_messages = {
        'foo': f'Unable to parse addr:port from "{specification}".',
        'foo:bar': f'Unable to parse addr:port from "{specification}". Unable to parse port.'
    }

    try:
        host = testinfra_bdd.fixture.get_host_fixture('docker://sut')
        host.get_resource_from_host('address and port', specification)
    except ValueError as ex:
        exception_raised = True
        actual_message = str(ex)
        assert actual_message == expected_messages[specification]

    assert exception_raised, 'Expected an exception to be raised.'
