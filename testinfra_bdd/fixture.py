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
        if timeout:
            self.wait_until_is_host_ready(timeout)

        try:
            self.host.system_info.type
            self.arch = self.host.system_info.arch
            self.codename = self.host.system_info.codename
            self.distribution = self.host.system_info.distribution
            self.hostname = self.host.backend.hostname
            self.release = self.host.system_info.release
            self.type = self.host.system_info.type
            is_ready = True
        except AssertionError:
            is_ready = False

        return is_ready

    def wait_until_is_host_ready(self, timeout=0):
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
            is_ready = self.is_host_ready()

            if now < deadline and not is_ready:
                time.sleep(1)

            now = time.time()

        return is_ready
