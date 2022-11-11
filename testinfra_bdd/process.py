"""
Then process fixtures for testinfra-bdd.

Please avoid already-imported warning: PYTEST_DONT_REWRITE.
"""
from pytest_bdd import (
    then,
    parsers,
    when
)

from testinfra_bdd.parsers import parse_process_filters


@when(parsers.parse('the process filter is {process_specification}'))
def the_process_filter_is(process_specification, testinfra_bdd_host):
    """
    Check the status of processes.

    Parameters
    ----------
    process_specification : str
        The process specification (e.g. "user=root,comm=ntpd").
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.
    """
    process_specification = process_specification.strip('"')
    testinfra_bdd_host.process_specification = process_specification
    host = testinfra_bdd_host.host
    testinfra_bdd_host.processes = host.process.filter(**parse_process_filters(process_specification))


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
