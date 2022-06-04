"""Basic string parsers for Testinfra BDD."""


def parse_addr_and_port(addr_and_port, host):
    """
    Parse a string containing an address and port.

    Parameters
    ----------
    addr_and_port : str
        The address and port in the format of "host:port".
    host : testinfra.host
        The relevant host.

    Returns
    -------
    tuple
        str the address, int the port number.

    Raises
    ------
    ValueError
        If the string can't be parsed.
    """
    strings = addr_and_port.split(':')
    message = f'Unable to parse addr:port from "{addr_and_port}".'

    if len(strings) != 2:
        raise ValueError(message)

    addr = strings[0]

    try:
        port_number = int(strings[1])
    except ValueError:
        raise ValueError(message + ' Unable to parse port.')

    address = host.addr(addr)
    port = address.port(port_number)
    return address, port, port_number


def parse_process_filters(specification):
    """
    Parse the process filters into a dictionary.

    Parameters
    ----------
    specification : str
        The process specifications to be parsed.

    Returns
    -------
    dict
        A dictionary of the parsed filters.

    Raises
    ------
    ValueError
        If the specification can't be parsed.
    """
    filters = {}

    for keypair in specification.split(','):
        keypair = keypair.split('=')

        if len(keypair) != 2:
            raise ValueError(f'Unable to parse process filters "{specification}".')

        key = keypair[0]
        value = keypair[1]
        filters[key] = value

    return filters
