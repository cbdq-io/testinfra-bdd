"""Dynamic configuration for setuptools."""
import os
import setuptools

try:
    import testinfra_bdd
    version = testinfra_bdd.__version__
except ModuleNotFoundError:
    version = os.environ['VERSION']

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()


install_requires = []

with open('pyproject.toml') as stream:
    pyproject = stream.readlines()

for line in pyproject:
    line = line.strip()[1:-2]

    if line.startswith('jmespath>') or line.startswith('pytest-bdd>') or line.startswith('pytest-testinfra>'):
        install_requires.append(line)

setuptools.setup(
    name='testinfra-bdd',
    version=version,
    author='Cloud Based DQ Ltd.',
    author_email='info@cbdq.io',
    description='An interface between pytest-bdd and pytest-testinfra.',
    install_requires=install_requires,
    keywords='testinfra,bdd',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cbdq-io/testinfra-bdd',
    project_urls={
        'Bug Tracker': 'https://github.com/cbdq-io/testinfra-bdd/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
    ],
    package_dir={'': '.'},
    packages=setuptools.find_packages(where='.'),
    python_requires='>=3.6')
