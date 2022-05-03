"""
An interface between pytest-bdd and pytest-testinfra.

For documentation and examples, please go to
https://github.com/locp/testinfra-bdd
"""
import pytest
import testinfra
import time

from pytest_bdd import (
    given,
    when,
    parsers
)

"""The version of the module.

This is used by setuptools and by gitchangelog to identify the name of the name
of the release.
"""
__version__ = '0.0.2'


def get_host_from_fixture(testinfra_bdd_host):
    """
    Return a Testinfra host object from the fixture.

    Parameters
    ----------
    testinfra_bdd_host : dict
        The dictionary must contain a key called "testinfra_host_url" which
        contains the URL of the host to connect to.

    Returns
    -------
    testinfra.host.Host
        A host object for connecting to the specified URL.
    """
    url = testinfra_bdd_host['testinfra_host_url']
    host = testinfra.get_host(url)
    return host


def is_host_ready(host, timeout=0):
    """
    Check if a host is ready within a specified time.

    Will poll the host every second until timeout number of seconds have
    expired.  If this host has not responded within that time, the host
    is assumed to not be ready.

    Parameters
    ----------
    host : testinfra.host.Host
        The host that should be checked for its readiness.
    timeout : int,optional
        The time in seconds to wait for the host to become ready.  The
        default is zero.

    Returns
    -------
    bool
        True if the host is responding to the host.system_info.type request.
        False if it doesn't.
    """
    is_ready = False
    now = time.time()
    deadline = now + timeout

    while now <= deadline and not is_ready:
        try:
            host.system_info.type
            is_ready = True
        except AssertionError:
            if now < deadline:
                time.sleep(1)

        now = time.time()

    return is_ready


@given(parsers.parse('Testinfra URL is {url}'), target_fixture='testinfra_bdd_host')
def testinfra_url_is_url(url):
    """
    Testinfra URL is <url>.

    Parameters
    ----------
    url : str
        The URL of the System Under Test (SUT).  Must comply to the Testinfra
        URL patterns.  See
        https://testinfra.readthedocs.io/en/latest/backends.html

    Returns
    -------
    dict
        A dictionary containing an element called testinfra_host_url which is
        set to the provided URL.
    """
    return {
        'testinfra_host_url': url
    }


@when(parsers.parse('Testinfra host arch is {expected_arch} or skip tests'))
def testinfra_host_arch_is_x86_64_or_skip_tests(expected_arch, testinfra_bdd_host):
    """Testinfra host arch is x86_64 or skip tests."""
    host = get_host_from_fixture(testinfra_bdd_host)
    actual_arch = host.system_info.arch
    message = f'Host arch ({actual_arch}) does not match {expected_arch}.'

    if actual_arch != expected_arch:
        pytest.skip(message)


@when(parsers.parse('Testinfra host codename is {expected_codename} or skip tests'))
def testinfra_host_codename_is_bullseye_or_skip_tests(expected_codename, testinfra_bdd_host):
    """Testinfra host codename is bullseye or skip tests."""
    host = get_host_from_fixture(testinfra_bdd_host)
    actual_codename = host.system_info.codename
    message = f'Host codename ({actual_codename}) does not match {expected_codename}.'

    if actual_codename != expected_codename:
        pytest.skip(message)


@when(parsers.parse('Testinfra host distribution is {expected_distribution} or skip tests'))
def testinfra_host_distribution_is_debian_or_skip_tests(expected_distribution, testinfra_bdd_host):
    """Testinfra host distribution is debian or skip tests."""
    host = get_host_from_fixture(testinfra_bdd_host)
    actual_distribution = host.system_info.distribution
    message = f'Host distribution ({actual_distribution}) does not match {expected_distribution}.'

    if actual_distribution != expected_distribution:
        pytest.skip(message)


@when('Testinfra host is ready')
def testinfra_host_is_ready(testinfra_bdd_host):
    """
    Testinfra host is ready.

    Check if a host is available now.  If not, don't wait and mark the tests
    as failed.

    Parameters
    ----------
    testinfra_bdd_host : dict
        The dictionary must contain a key called "testinfra_host_url" which
        contains the URL of the host to connect to.
    """
    url = testinfra_bdd_host['testinfra_host_url']
    host = get_host_from_fixture(testinfra_bdd_host)
    is_ready = is_host_ready(host)
    message = f'Host {url} is not become ready.'
    assert is_ready, message


@when('Testinfra host is ready or skip tests')
def testinfra_host_is_ready_or_skip_tests(testinfra_bdd_host):
    """
    Testinfra host is ready or skip tests.

    Check if a host is available now.  If not, don't wait, just skip the
    tests.

    Parameters
    ----------
    testinfra_bdd_host : dict
        The dictionary must contain a key called "testinfra_host_url" which
        contains the URL of the host to connect to.
    """
    url = testinfra_bdd_host['testinfra_host_url']
    host = get_host_from_fixture(testinfra_bdd_host)
    is_ready = is_host_ready(host)

    if not is_ready:
        pytest.skip(f'Host {url} is not ready.')


@when(parsers.parse('Testinfra host is ready within {seconds:d} seconds'))
def testinfra_host_is_ready_within_10_seconds(seconds, testinfra_bdd_host):
    """Testinfra host is ready within <seconds> seconds."""
    url = testinfra_bdd_host['testinfra_host_url']
    host = get_host_from_fixture(testinfra_bdd_host)
    is_ready = is_host_ready(host, seconds)
    message = f'Host {url} did not become ready within {seconds} seconds.'
    assert is_ready, message


@when(parsers.parse('Testinfra host is ready within {seconds:d} seconds or skip tests'))
def testinfra_host_is_ready_within_seconds_seconds_or_skip_tests(seconds, testinfra_bdd_host):
    """Testinfra host is ready within <seconds> seconds or skip tests."""
    url = testinfra_bdd_host['testinfra_host_url']
    host = get_host_from_fixture(testinfra_bdd_host)
    is_ready = is_host_ready(host, seconds)

    if not is_ready:
        pytest.skip(f'Host {url} is not ready.')


@when(parsers.parse('Testinfra host release is {expected_release} or skip tests'))
def testinfra_host_release_is_102_or_skip_tests(expected_release, testinfra_bdd_host):
    """Testinfra host release is <expected_release> or skip tests."""
    host = get_host_from_fixture(testinfra_bdd_host)
    actual_release = host.system_info.release
    message = f'Host release ({actual_release}) does not match {expected_release}.'

    if actual_release != expected_release:
        pytest.skip(message)


@when(parsers.parse('Testinfra host type is {expected_type} or skip tests'))
def testinfra_host_type_is_linux_or_skip_tests(expected_type, testinfra_bdd_host):
    """Testinfra host type is linux or skip tests."""
    host = get_host_from_fixture(testinfra_bdd_host)
    actual_type = host.system_info.type
    message = f'Host type ({actual_type}) does not match {expected_type}.'

    if actual_type != expected_type:
        pytest.skip(message)
