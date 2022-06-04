"""Functions required for Pip packages."""

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
