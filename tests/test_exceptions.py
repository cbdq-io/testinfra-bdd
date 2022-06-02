"""Test exceptions are raised as expected."""
import testinfra_bdd


def test_invalid_resource_type():
    """Test that an exception is thrown when attempting to get an invalid resource type."""
    exception_raised = False

    try:
        host = testinfra_bdd.TestinfraBDD('docker://sut')
        host.get_resource_from_host('foo', 'foo')
    except AssertionError as ex:
        exception_raised = True
        assert str(ex) == 'Unknown resource type "foo".'

    assert exception_raised, 'Expected an exception to be raised.'


def test_invalid_command_stream_name():
    """Test that an exception is thrown when attempting to get an invalid resource type."""
    exception_raised = False

    try:
        host = testinfra_bdd.TestinfraBDD('docker://sut')
        host.get_resource_from_host('command', 'ls')
        host.get_stream_from_command('foo')
    except ValueError as ex:
        exception_raised = True
        assert str(ex) == 'Unknown stream name "foo".'

    assert exception_raised, 'Expected an exception to be raised.'


def test_unready_host():
    """Test that a non-ready host throws an exception."""
    host = testinfra_bdd.TestinfraBDD('docker://foo')
    assert not host.is_host_ready(1)


def test_superseded_pip_package():
    """Test that a superseded pip package is identified."""
    exception_raised = False

    try:
        host = testinfra_bdd.TestinfraBDD('docker://sut')
        host.get_resource_from_host('pip package', 'semver')
        testinfra_bdd.the_pip_package_state_is('latest', host)
    except AssertionError as ex:
        exception_raised = True
        assert str(ex) == 'Expected pip package semver to be latest but it is superseded.'

    assert exception_raised, 'Expected an exception to be raised.'
