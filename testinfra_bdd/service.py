"""Then service fixtures for testinfra-bdd."""
from pytest_bdd import parsers
from pytest_bdd import then
from pytest_bdd import when


@when(parsers.parse('the service is {service}'))
def the_service_is(service: str, testinfra_bdd_host):
    """
    Check the status of a service.

    Parameters
    ----------
    service : str
        The service name (e.g. "named").
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.
    """
    testinfra_bdd_host.service = testinfra_bdd_host.host.service(service.strip('"'))


@then('the service is not enabled')
def the_service_is_not_enabled(testinfra_bdd_host):
    """
    Check that the service is not enabled.

    Parameters
    ----------
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        When the service is enabled.
    """
    service = testinfra_bdd_host.service
    message = f'Expected {service.name} on host {testinfra_bdd_host.hostname} to be disabled, but it is enabled.'
    assert not service.is_enabled, message


@then('the service is enabled')
def the_service_is_enabled(testinfra_bdd_host):
    """
    Check that the service is enabled.

    Parameters
    ----------
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        When the service is not enabled.
    """
    service = testinfra_bdd_host.service
    message = f'Expected {service.name} on host {testinfra_bdd_host.hostname} to be enabled, but it is disabled.'
    assert service.is_enabled, message


@then('the service is not running')
def the_service_is_not_running(testinfra_bdd_host):
    """
    Check that the service is not running.

    Parameters
    ----------
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        When the service is running.
    """
    service = testinfra_bdd_host.service
    message = f'Expected {service.name} on host {testinfra_bdd_host.hostname} to not be running.'
    assert not service.is_running, message


@then('the service is running')
def the_service_is_running(testinfra_bdd_host):
    """
    Check that the service is running.

    Parameters
    ----------
    testinfra_bdd_host : testinfra_bdd.fixture.TestinfraBDD
        The test fixture.

    Raises
    ------
    AssertError
        When the service is not running.
    """
    service = testinfra_bdd_host.service
    message = f'Expected {service.name} on host {testinfra_bdd_host.hostname} to be running.'
    assert service.is_running, message
