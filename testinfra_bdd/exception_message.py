"""File exception_message.py."""


def exception_message(resource_name, actual_state, expected_state):
    """
    Format a message suitable for an exception message.

    Parameters
    ----------
    resource_name : str
        The name of the relevant resource (e.g. "package foo").
    actual_state : str
        The actual state of the resource (e.g. absent).
    expected_state : str
        The expected state of the resource (e.g. present).

    Returns
    -------
    str
        A string suitable for passing to an exception (e.g. "Expected package foo to be present but it is absent.").
    """
    return f'Expected {resource_name} to be {expected_state} but it is {actual_state}.'
