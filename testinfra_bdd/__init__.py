"""
An interface between pytest-bdd and pytest-testinfra.

For documentation and examples, please go to
https://github.com/locp/testinfra-bdd
"""
# import testinfra

from pytest_bdd import given
from pytest_bdd import parsers

"""The version of the module.

This is used by setuptools and by gitchangelog to identify the name of the name
of the release.
"""
__version__ = '0.0.2'


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
