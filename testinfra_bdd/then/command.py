"""Then command fixtures for testinfra-bdd."""
import re

from pytest_bdd import parsers
from pytest_bdd import then


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


@then(parsers.parse('the command {stream_name} contains the expected value'))
def the_command_stderr_contains_the_expected_value(stream_name, expected_value, testinfra_bdd_host):
    """
    Check that the stdout or stderr stream contains a pre-defined expected value.

    Parameters
    ----------
    stream_name : str
        The name of the stream to check.  Must be "stdout" or "stderr".
    expected_value : A pytest fixture.
        This is pre-defined by the user.
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        When the specified stream does not contain the expected text.
    """
    stream = testinfra_bdd_host.get_stream_from_command(stream_name)
    message = f'The string "{expected_value}" was not found in the {stream_name} ("{stream}") of the command.'
    assert expected_value in stream, message


@then(parsers.parse('the command {stream_name} does not contain "{text}"'))
def the_command_stdout_does_not_contain_foo(stream_name, text, testinfra_bdd_host):
    """
    Check that the stdout or stderr stream does not contain a string.

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
        When the specified stream does contain the unexpected text.
    """
    stream = testinfra_bdd_host.get_stream_from_command(stream_name)
    message = f'The unexpected string "{text}" was found in the {stream_name} ("{stream}") of the command.'
    assert text not in stream, message


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
