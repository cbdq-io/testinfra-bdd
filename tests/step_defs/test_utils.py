"""Test the utility functions feature tests."""
import json

import testinfra

from pytest_bdd import (
    given,
    scenario,
    then,
    when,
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


# Ensure that the PyTest fixtures provided in testinfra-bdd are available to
# your test suite.
pytest_plugins = ['testinfra_bdd']


@scenario('utils.feature', 'Expect Unready Host')
def test_expect_unready_host():
    """Expect Unready Host."""


@scenario('utils.feature', 'Get System Properties')
def test_get_system_properties():
    """Get System Properties."""


@scenario('utils.feature', 'Request for Invalid Resource Should Fail')
def test_request_for_invalid_resource_should_fail():
    """Request for Invalid Resource Should Fail."""


@scenario('utils.feature', 'Test Get Host from Fixture')
def test_test_get_host_from_fixture():
    """Test Get Host from Fixture."""


@scenario('utils.feature', 'Unknown stream name for a command')
def test_unknown_stream_name_for_a_command():
    """Unknown stream name for a command."""


@given(parsers.parse('JSON text is "{json_string}"'), target_fixture='mock_host')
def json_text(json_string):
    """Given JSON text is <json_string>."""
    return json.loads(json_string)


@given(parsers.parse('a host specification of "{hostspec}"'), target_fixture='testinfra_bdd_host')
def a_host_specification_of(hostspec):
    """a host specification of "docker://foo"."""
    return {
        'url': hostspec,
        'host': testinfra.get_host(hostspec)
    }


@when('text is passed as a dict to get_resource_from_fixture')
def text_is_passed_as_a_dict_to_get_host_from_fixture():
    """text is passed as a dict to get_host_from_fixture."""
    pass


@when('a resource called "foo" is requested')
def a_resource_called_foo_is_requested():
    """a resource called "foo" is requested."""
    pass


@when(parsers.parse('"{property_name}" is requested from the host'))
def the_value_of_property_name_is_requested(property_name, testinfra_bdd_host):
    """the value of <property_name> is requested."""
    testinfra_bdd_host['property_name'] = property_name


@then(parsers.parse('expect "{exception_message}" as a ValueError'))
def expect_exception_message_as_a_valueerror(exception_message, mock_host):
    """expect "<exception_message>" as a ValueError."""
    try:
        get_resource_from_fixture(mock_host, 'foo')
    except RuntimeError as ex:
        actual_exception_message = str(ex)
    except ValueError as ex:
        actual_exception_message = str(ex)

    message = f'Expected "{exception_message}" as the exception message but got "{actual_exception_message}".'
    assert actual_exception_message == exception_message, message


@then('expect an exception from stream name of "foo"')
def expect_an_exception_from_stream_name_of_foo(testinfra_bdd_host):
    """expect an exception from stream name of "foo"."""
    host = get_host_from_fixture(testinfra_bdd_host)
    cmd = get_resource_from_host(host, 'command', 'java -version')
    try:
        get_stream_from_command(cmd, 'foo')
    except ValueError as ex:
        exception_message = str(ex)

    assert exception_message == 'Unknown stream name "foo".'


@then('expect the host to be unready')
def expect_the_host_to_be_unready(testinfra_bdd_host):
    """expect the host to be unready."""
    host = testinfra_bdd_host['host']
    message = f'Expected {host.backend.get_pytest_id()} to not be ready.'
    assert not is_host_ready(host, 1), message


@then(parsers.parse('status should be {status}'))
def status_should_be_status(status, testinfra_bdd_host):
    """status should be <status>."""
    if status == 'OK':
        expected_status = True
    else:
        expected_status = False

    try:
        get_host_property(testinfra_bdd_host['host'], testinfra_bdd_host['property_name'])
        actual_status = True
    except ValueError:
        actual_status = False

    assert actual_status == expected_status


@then('the ValueError exception will be \'Unknown resource type "foo".\'')
def the_valueerror_exception_will_be_unknown_resource_type_foo(testinfra_bdd_host):
    """the ValueError exception will be 'Unknown resource type "foo".'."""
    host = get_host_from_fixture(testinfra_bdd_host)

    try:
        get_resource_from_host(host, 'foo', 'foo')
        exception_message = ''
    except ValueError as ex:
        exception_message = str(ex)

    assert exception_message == 'Unknown resource type "foo".'
