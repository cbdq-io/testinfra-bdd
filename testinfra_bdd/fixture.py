"""The main fixture for the testinfra-bdd tests."""
import time

import testinfra


class TestinfraBDD:
    """A class that is used as the fixture in the given/when/then steps."""

    def __init__(self, url):
        """
        Create a TestinfraBDD object.

        Initialises the host attribute.

        Parameters
        ----------
        url : str
            The URL of the System Under Test (SUT).  Must comply to the Testinfra
            URL patterns.  See https://testinfra.readthedocs.io/en/latest/backends.html
        """
        self.address = None
        self.arch = None
        self.codename = None
        self.command = None
        self.distribution = None
        self.file = None
        self.group = None
        self.host = testinfra.get_host(url)
        self.hostname = None
        self.package = None
        self.pip_package = None
        self.port = None
        self.port_number = None
        self.process_specification = None
        self.processes = None
        self.release = None
        self.service = None
        self.socket = None
        self.socket_url = None
        self.type = None
        self.url = url
        self.user = None

    def get_host_property(self, property_name):
        """
        Get a named host property.

        Parameters
        ----------
        property_name : str
            The name of the property to be extracted.

        Raises
        ------
        AssertError
            If the property_name is invalid.

        Returns
        -------
        str
            The value of the property.
        """
        properties = {
            'type': self.host.system_info.type,
            'distribution': self.host.system_info.distribution,
            'release': self.host.system_info.release,
            'codename': self.host.system_info.codename,
            'arch': self.host.system_info.arch,
            'hostname': self.host.backend.get_hostname(),
            'connection_type': self.host.backend.NAME
        }

        assert property_name in properties, f'Invalid host property name "{property_name}".'
        return properties[property_name]

    def get_resource_from_host(self, resource_type, resource_name):
        """
        Use a Testinfra module to get a resource from the system under test.

        Parameters
        ----------
        resource_type : str
            The type of resource to be examined.
        resource_name : str
            The name of the resource to be examined.  If resource_type is "command" then this is the
            command line to be executed.

        Returns
        -------
        object
            The resource that has been requested.
        """
        resource_type_is_set = True

        if resource_type == 'command':
            self.command = self.host.run(resource_name)
        elif resource_type == 'service':
            self.service = self.host.service(resource_name)
        elif resource_type == 'package':
            self.package = self.host.package(resource_name)
        elif resource_type == 'file':
            self.file = self.host.file(resource_name)
        elif resource_type == 'user':
            self.user = self.host.user(resource_name)
        elif resource_type == 'group':
            self.group = self.host.group(resource_name)
        elif resource_type == 'pip package':
            self.pip_package = self.host.pip(resource_name)
        elif resource_type == 'process filter':
            self.process_specification = resource_name
            filters = self.parse_process_filters()
            self.processes = self.host.process.filter(**filters)
        elif resource_type == 'socket':
            self.socket = self.host.socket(resource_name)
        elif resource_type == 'address':
            self.address = self.host.addr(resource_name)
        elif resource_type == 'address and port':
            port = resource_name.split(':')
            assert len(port) == 2, f'Unable to parse addr:port from "{resource_name}".'
            address = port[0]
            address = self.host.addr(address)
            self.port_number = int(port[1])
            self.port = address.port(self.port_number)
            self.address = address
        else:
            resource_type_is_set = False

        assert resource_type_is_set, f'Unknown resource type "{resource_type}".'

    def get_stream_from_command(self, stream_name):
        """
        Get a named stream from the command.

        Parameters
        ----------
        stream_name : str
            The name of the stream.

        Raises
        ------
        AssertError
            If the command attribute is None.
        ValueError
            When the stream name is not recognized.

        Returns
        -------
        str
            The requested stream content.
        """
        assert self.command, 'No command has been executed.'

        if stream_name == 'stdout':
            return self.command.stdout
        elif stream_name == 'stderr':
            return self.command.stderr

        raise ValueError(f'Unknown stream name "{stream_name}".')

    def is_host_ready(self, timeout=0):
        """
        Check if a host is ready within a specified time.

        Will poll the host every second until timeout number of seconds have
        expired.  If this host has not responded within that time, the host
        is assumed to not be ready.

        Parameters
        ----------
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
                self.host.system_info.type
                is_ready = True
                self.arch = self.host.system_info.arch
                self.codename = self.host.system_info.codename
                self.distribution = self.host.system_info.distribution
                self.hostname = self.host.backend.hostname
                self.release = self.host.system_info.release
                self.type = self.host.system_info.type
            except AssertionError:
                if now < deadline:
                    time.sleep(1)

            now = time.time()

        return is_ready

    def parse_process_filters(self):
        """
        Parse the process filters into a dictionary.

        Raises
        ------
        ValueError
            If the specification can't be parsed.
        """
        filters = {}
        specification = self.process_specification

        for keypair in specification.split(','):
            keypair = keypair.split('=')

            if len(keypair) != 2:
                raise ValueError(f'Unable to parse process filters "{specification}".')

            key = keypair[0]
            value = keypair[1]
            filters[key] = value

        return filters


def get_host_fixture(hostspec, timeout=0):
    """
    Return a host that is confirmed as ready.

    hostspec : str
        The URL of the System Under Test (SUT).  Must comply to the Testinfra
        URL patterns.  See
        https://testinfra.readthedocs.io/en/latest/backends.html
    timeout : int, optional
        The number of seconds that the host is expected to become ready in.

    Returns
    -------
    testinfra_bdd.fixture.TestinfraBDD
        The object to return as a fixture.

    Raises
    ------
    AssertError
        When the host is not ready.
    """
    if timeout:
        message = f'The host {hostspec} is not ready within {timeout} seconds.'
    else:
        message = f'The host {hostspec} is not ready.'

    host = TestinfraBDD(hostspec)
    assert host.is_host_ready(timeout), message
    return host
