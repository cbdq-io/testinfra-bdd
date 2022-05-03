"""parametrized feature tests."""
import pytest

from pytest_bdd import (
    given,
    parsers,
    scenario
)

# Ensure that the PyTest fixtures provided in testinfra-bdd are available to
# your test suite.
pytest_plugins = ['testinfra_bdd']

"""A list of tuples containing host URLs."""
URL_LIST = [
    ('docker://sut',),
    ('docker://java11',)
]


# Here we use pytest to parametrize the test with a list of URLs.
@pytest.mark.parametrize(
    ['url'],
    URL_LIST
)
@scenario('../features/parametrized.feature', 'Parametrized URL')
def test_parametrized_url(url):
    """Parametrized URL."""


@given(parsers.parse('the Testinfra URL parameter is {url}'), target_fixture='testinfra_bdd_host')
def parametrized_url(url):
    """
    Provide an alternative "Given" step for a parametrized test.

    The "Given" step must return a target fixture called
    "testinfra_bdd_host" so that the rest of the Testinfra BDD fixtures will
    function.

    Parameters
    ----------
    url : str
        The Testinfra host URL to connect to.

    Returns
    -------
    dict
        The dictionary must contain a key called "testinfra_host_url" that
        contains the provided URL.
    """
    return {
        'testinfra_host_url': url
    }
