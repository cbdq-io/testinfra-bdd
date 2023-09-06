"""Then file fixtures for testinfra-bdd."""
import json
import re

import jmespath
from pytest_bdd import parsers, then, when

from testinfra_bdd.file_helpers import get_file_actual_state


@when(parsers.parse('the TestInfra file is {file_name}'))
def the_file_is(file_name: str, testinfra_bdd_host):
    """
    Check the status of a file.

    Parameters
    ----------
    file_name : str
        The package name (e.g. "/etc/motd").
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.
    """
    testinfra_bdd_host.file = testinfra_bdd_host.host.file(file_name.strip('"'))


@then(parsers.parse('the TestInfra file contents contains "{text}"'))
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


@then(parsers.parse('the TestInfra file contents contains the regex "{pattern}"'))
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


@then(parsers.parse('the TestInfra file is {expected_status}'))
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
    if expected_status == 'executable':
        property_name = 'executable'
    else:
        property_name = 'state'

    the_file_property_is(property_name, expected_status, testinfra_bdd_host)


@then(parsers.parse('the TestInfra file {property_name} is {expected_value}'))
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
    (actual_value, exception_message) = get_file_actual_state(
        testinfra_bdd_host.file,
        property_name,
        expected_value
    )
    assert actual_value == expected_value, exception_message


@then(parsers.parse('the TestInfra JMESPath expression {expression} returns {expected_value}'))
def the_jmespath_expression_expression_returns_expected_value(expression, expected_value, testinfra_bdd_host):
    """
    Check the contents of a JSON file with JMESPath.

    Parameters
    ----------
    expression : str
        A JMESPath expression.
    expected_value : str
        The value expected to be returned.  All values returned by JMESPath will
        be converted to a string before comparison.
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        If the file is not valid JSON or if the JMESPath expression returns
        another value other than the expected value.
    """
    file = testinfra_bdd_host.file
    file_name = f'{testinfra_bdd_host.hostname}:{file.path}'
    the_file_property_is('state', 'present', testinfra_bdd_host)
    the_file_property_is('type', 'file', testinfra_bdd_host)
    data = json.loads(file.content_string)
    actual_value = str(jmespath.search(expression, data))
    message = f'Expected {expression} in {file_name} to be "{expected_value}", but it is "{actual_value}".'
    assert actual_value == expected_value, message
