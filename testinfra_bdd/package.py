"""Then system package fixtures for testinfra-bdd."""
from pytest_bdd import parsers, then, when

from testinfra_bdd import TestinfraBDD


@when(parsers.parse('the TestInfra package is {package_name}'))
def the_package_is(package_name: str, testinfra_bdd_host):
    """
    Check the status of a package.

    Parameters
    ----------
    package_name : str
        The package name (e.g. "python3").
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.
    """
    testinfra_bdd_host.package = testinfra_bdd_host.host.package(package_name.strip('"'))


@then(parsers.parse('the TestInfra package version will be greater than or equal to {expected_version}'))
def _(expected_version: str, testinfra_bdd_host: TestinfraBDD):
    """
    Check that a system package is higher than the specified version.

    Parameters
    ----------
    expected_version : str
        The expected version of the package.
    testinfra_bdd_host : TestinfraBDD
        The details of the host that we're testing against.

    Raises
    ------
    AssertionError
        The actual version of the package doesn't meed expectations.
    """
    actual_version = testinfra_bdd_host.package.version
    message = f'Expected {testinfra_bdd_host.package.name} to be >= "{expected_version}", '
    message += f'but it is "{actual_version}".'
    assert actual_version >= expected_version, message


@then(parsers.parse('the TestInfra package state is {expected_status}'))
@then(parsers.parse('the TestInfra package is {expected_status}'))
def the_package_status_is(expected_status, testinfra_bdd_host):
    """
    Check the status of a package (installed/absent).

    Parameters
    ----------
    expected_status : str
        Can be absent, installed or present.
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
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
    else:
        message = f'Expected {pkg.name} to be absent on {testinfra_bdd_host.hostname} '
        message += 'but it is installed ({pkg.version}).'

    assert actual_status == expected_to_be_installed, message
