"""Tests Expected to Fail feature tests."""
import testinfra
import testinfra_bdd

from pytest_bdd import (
    given,
    scenario,
    when,
)


@scenario('../features/xfail.feature', 'Host Not Available')
def test_host_not_available():
    """Host Not Available."""


@scenario('../features/xfail.feature', 'Host Not Available Within a Time')
def test_host_not_available_within_a_time():
    """Host Not Available Within a Time."""


@given('the Testinfra URL is docker://snafu', target_fixture='host')
def the_testinfra_url_is_dockersnafu():
    """the Testinfra URL is docker://snafu."""
    return testinfra.get_host('docker://snafu')


@when('host is not ready within 2 seconds')
def host_is_not_ready_within_2_seconds(host):
    """host is not ready within 2 seconds."""
    assert not testinfra_bdd.is_host_ready(host, 2)


@when('host is ready')
def host_is_ready(host):
    """host is ready."""
    assert not testinfra_bdd.is_host_ready(host)
