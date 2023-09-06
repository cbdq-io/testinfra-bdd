"""Helper functions for the file fixtures for testinfra-bdd."""


from testinfra_bdd.exception_message import exception_message


def get_file_actual_state(file, property_name, expected_state):
    """
    Get the actual state of a file given the package and the expected state.

    Parameters
    ----------
    file : testinfra.File
        The file to be checked.
    property_name : str
        The name of the property to check (e.g. state).
    expected_state : str
        The expected state.

    Returns
    -------
    tuple
        str
            The actual state (e.g. absent, latest, present or superseded).
        str
            A suitable message if the actual state doesn't match the actual state.
    """
    properties = get_file_properties(file)
    assert property_name in properties, f'Unknown user property "{property_name}".'
    actual_state = properties[property_name]
    return actual_state, exception_message(f'File {file.path} {property_name}', actual_state, expected_state)


def get_file_properties(file):
    """
    Get the properties of the file.

    Parameters
    ----------
    file : testinfra.File
        The file to be checked.

    Returns
    -------
    dict
        A dictionary of the properties.
    """
    assert file, 'File not set.  Have you missed a "When file is" step?'
    properties = {
        'executable': None,
        'group': None,
        'mode': None,
        'owner': None,
        'state': 'absent',
        'type': None,
        'user': None
    }

    executable_states = {
        True: 'executable',
        False: 'not executable'
    }

    if file.exists:
        properties = {
            'executable': executable_states[file.is_executable],
            'group': file.group,
            'mode': '0o%o' % file.mode,
            'owner': file.user,
            'state': 'present',
            'type': get_file_type(file),
            'user': file.user
        }

    return properties


def get_file_type(file):
    """
    Get the file type.

    Parameters
    ----------
    file : testinfra.File
        The file to be checked.

    Returns
    -------
    str
        The type of file.
    """
    file_type = None

    type_lookup = {
        'file': file.is_file,
        'directory': file.is_directory,
        'pipe': file.is_pipe,
        'socket': file.is_socket,
        'symlink': file.is_symlink
    }

    for key in type_lookup:
        if type_lookup[key]:
            file_type = key
            break

    return file_type
