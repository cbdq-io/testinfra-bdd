"""Dynamic configuration for setuptools."""
import setuptools

import testinfra_bdd

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

version = testinfra_bdd.__version__

setuptools.setup(
    name='testinfra-bdd',
    version=version,
    author='League of Crafty Programmers Ltd.',
    author_email='info@locp.co.uk',
    description='An interface between pytest-bdd and pytest-testinfra.',
    install_requires=['pytest-bdd>=5.00<=6.0.0', 'pytest-testinfra>=6.0.0<=7.0.0'],
    keywords='testinfra,bdd',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/locp/testinfra-bdd',
    project_urls={
        'Bug Tracker': 'https://github.com/locp/testinfra-bdd/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
    ],
    package_dir={'': '.'},
    packages=setuptools.find_packages(where='.'),
    python_requires='>=3.6')
