"""Configure pytest_plugins."""
global pytest_plugins


def add_plugins():
    """
    Add missing plugins to pytest_plugins.

    Returns
    -------
    list
        The value to set pytest_plugins to.
    """
    if 'pytest_plugins' in globals():
        plugins = globals()
    else:
        plugins = []

    for plugin in ['testinfra_bdd.given']:
        if plugin not in plugins:
            plugins.append(plugin)

    return plugins
