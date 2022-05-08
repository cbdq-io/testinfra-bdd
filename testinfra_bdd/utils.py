"""Utility functions for Testinfra BDD."""
import time


def get_host_from_fixture(testinfra_bdd_host):
    """
    Return the host from the test fixture.

    This function also validates that the test fixture has been constructed correctly.

    Parameters
    ----------
    testinfra_bdd_host : dict
        The test fixture.

    Returns
    -------
    testinfra.host.Host
        The host contained in the fixture.
    """
    if 'url' not in testinfra_bdd_host:
        raise ValueError('Badly constructed test fixture.  Missing the host "url".')
    elif 'host' not in testinfra_bdd_host:
        raise ValueError('Badly constructed test fixture.  Missing the "host".')

    return testinfra_bdd_host['host']


def get_host_property(host, property_name):
    """
    Get a property from the Testinfra SystemInfo module.

    Valid values for the property name are:
        - type (e.g. "linux").
        - distribution (e.g. "debian").
        - release (e.g. "10.2").
        - codename (e.g. "bullseye").
        - arch (e.g. "x86_64").

    Parameters
    ----------
    host : testinfra.host.Host
        The host to extract the property from.
    property_name : str
        The name of the property to get.

    Raises
    ------
    ValueError
        If the property name is invalid.

    Returns
    -------
    str
        The value of the property requested.
    """
    properties = {
        'type': host.system_info.type,
        'distribution': host.system_info.distribution,
        'release': host.system_info.release,
        'codename': host.system_info.codename,
        'arch': host.system_info.arch,
        'hostname': host.backend.get_hostname()
    }

    try:
        return properties[property_name]
    except KeyError:
        raise ValueError(f'Unknown property name {property_name}.')


def get_resource_from_fixture(testinfra_bdd_host, resource_type):
    """
    Get the command object from the suite fixture.

    Parameters
    ----------
    testinfra_bdd_host : dict
        The test fixture.
    resource_type : str
        The resource type to return.

    Returns
    -------
    testinfra.backend.base.CommandResult
        The command result.

    Raises
    ------
    RuntimeError
        If the resource type is not present in the fixture.
    """
    # Validate the fixture before we do anything.
    get_host_from_fixture(testinfra_bdd_host)

    if resource_type not in testinfra_bdd_host:
        raise RuntimeError(f'Resource "{resource_type}" not found.  Did you miss a "When" step?')
    return testinfra_bdd_host[resource_type]


def get_resource_from_host(host, resource_type, resource_name):
    """
    Use a Testinfra module to get a resource from the system under test.

    Parameters
    ----------
    host : testinfra.host.Host
        The host to extract the property from.

    Returns
    -------
    object
        The resource that has been requested.
    """
    if resource_type == 'command':
        return host.run(resource_name)
    elif resource_type == 'service':
        return host.service(resource_name)
    elif resource_type == 'package':
        return host.package(resource_name)
    elif resource_type == 'file':
        return host.file(resource_name)

    raise ValueError(f'Unknown resource type "{resource_type}".')


def get_stream_from_command(command, stream_name):
    """
    Get the specified stream content from the provided command.

    Parameters
    ----------
    command : testinfra.backend.base.CommandResult
        The provided command to get the stream content from.
    stream_name : str
        The name of the stream.

    Raises
    ------
    ValueError
        When the stream name is not recognized.

    Returns
    -------
    str
        The requested stream content.
    """
    if stream_name == 'stdout':
        return command.stdout
    elif stream_name == 'stderr':
        return command.stderr

    raise ValueError(f'Unknown stream name "{stream_name}".')


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
