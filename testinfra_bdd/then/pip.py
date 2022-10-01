"""
Then pip package fixtures for testinfra-bdd.

Please avoid already-imported warning: PYTEST_DONT_REWRITE.
"""
from pytest_bdd import (
    then,
    parsers
)

from testinfra_bdd.exception_message import exception_message


def check_entry_requirements(pip_package, expected_state):
    """
    Check that the entry requirements are met for the test.

    Parameters
    ----------
    pip_package : testinfra.Pip
        The Pip package to be checked.
    expected_state : str
        The expected state.

    Raises
    ------
    ValueError
        If the expected state is invalid.
    RuntimeError
        If the Pip package has not been set.
    """
    valid_expected_states = [
        'absent',
        'latest',
        'present',
        'superseded'
    ]

    if expected_state not in valid_expected_states:
        raise ValueError(f'Unknown expected state "{expected_state}" for a Pip package.')
    elif not pip_package:
        raise RuntimeError('Pip package not set.  Have you missed a "When pip package is" step?')


def get_pip_package_actual_state(pip_package, expected_state, host):
    """
    Get the actual state of a Pip package given the package and the expected state.

    Parameters
    ----------
    pip_package : testinfra.Pip
        The Pip package to be checked.
    expected_state : str
        The expected state.
    host : testinfra.host.Host
        The host to be checked against.

    Returns
    -------
    tuple
        str
            The actual state (e.g. absent, latest, present or superseded).
        str
            A suitable message if the actual state doesn't match the actual state.
    """
    state_checks = [
        'absent',
        'present'
    ]

    check_entry_requirements(pip_package, expected_state)

    if expected_state in state_checks:
        actual_state = 'absent'

        if pip_package.is_installed:
            actual_state = 'present'

        return actual_state, exception_message(
            f'Pip package {pip_package.name}',
            actual_state,
            expected_state
        )

    outdated_packages = host.pip.get_outdated_packages()

    if pip_package.name in outdated_packages:
        actual_state = 'superseded'
    else:
        actual_state = 'latest'

    return actual_state, exception_message(f'Pip package {pip_package.name}', actual_state, expected_state)


@then('the pip check is OK')
def the_pip_check_is_ok(testinfra_bdd_host):
    """
    Verify installed packages have compatible dependencies.

    Parameters
    ----------
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        When the packages have incompatible dependencies.
    """
    host = testinfra_bdd_host.host
    cmd = host.pip.check()
    message = f'Incompatible Pip packages - {cmd.stdout} {cmd.stderr}'
    assert cmd.rc == 0, message


@then(parsers.parse('the pip package state is {expected_state}'))
@then(parsers.parse('the pip package is {expected_state}'))
def the_pip_package_state_is(expected_state, testinfra_bdd_host):
    """
    Check the state of a Pip package.

    Parameters
    ----------
    expected_state : str
        The expected state of the package.  Can be absent, latest or installed.
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        When the actual state doesn't match the expected state.
    """
    (actual_state, message) = get_pip_package_actual_state(
        testinfra_bdd_host.pip_package,
        expected_state,
        testinfra_bdd_host.host
    )
    assert actual_state == expected_state, message


@then(parsers.parse('the pip package version is {expected_version}'))
def the_pip_package_version_is(expected_version, testinfra_bdd_host):
    """
    Check the version of a Pip package.

    Parameters
    ----------
    expected_version : str
        The version of the package that is expected.
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        When the actual version is not the expected version.
    """
    pip_package = testinfra_bdd_host.pip_package
    assert pip_package, 'Pip package not set.  Have you missed a "When pip package is" step?'
    actual_version = pip_package.version
    message = f'Expected Pip package version to be {expected_version} but it was {actual_version}.'
    assert actual_version == expected_version, message
