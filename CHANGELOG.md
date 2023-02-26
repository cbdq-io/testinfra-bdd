# Changelog


## 2.2.5

### Fix

* Migrate from League of Crafty Programmers to Cloud Based DQ. [Ben Dalling]

* Tests/resources/requirements-latest.txt to reduce vulnerabilities. [snyk-bot]

  The following vulnerabilities are fixed by pinning transitive dependencies:
  - https://snyk.io/vuln/SNYK-PYTHON-SETUPTOOLS-3180412


## 2.2.4 (2022-12-31)

### New

* Successfully tested compliance against pytest-testinfra 7. [Ben Dalling]

### Fix

* Requirements.txt to reduce vulnerabilities. [snyk-bot]

  The following vulnerabilities are fixed by pinning transitive dependencies:
  - https://snyk.io/vuln/SNYK-PYTHON-GITPYTHON-3113858

* Correct issues identified by CodeQL. [Ben Dalling]

* Requirements.txt to reduce vulnerabilities. [snyk-bot]

  The following vulnerabilities are fixed by pinning transitive dependencies:
  - https://snyk.io/vuln/SNYK-PYTHON-SETUPTOOLS-3113904

### Other

* Add CodeQL workflow for GitHub code scanning. [LGTM Migrator]


## 2.2.3 (2022-11-11)

### Fix

* Refactor "When" steps after update to pytest-bdd. [Ben Dalling]


## 2.2.2 (2022-11-09)

### Fix

* Temporary work around until problem with pytest-bdd>=6.1.0 is fixed. [Ben Dalling]


## 2.2.1 (2022-10-18)

### Fix

* Ensure JMESPath is installed as a requirement. [Ben Dalling]


## 2.2.0 (2022-10-15)

### New

* Allow JMESPath interrogation of files. [Ben Dalling]


## 2.1.0 (2022-10-01)

### New

* Add documentation for the expected_value fixture. [Ben Dalling]

* Add a check to ensure text is absent from a command stream. [Ben Dalling]

* Add the expected_value fixture. [Ben Dalling]

### Fix

* Suppress already-imported warning: PYTEST_DONT_REWRITE. [Ben Dalling]

* The python-flake8 (1.1.1) package is not compatible with flake8 >= 5.0.0. [Ben Dalling]


## 2.0.0 (2022-07-21)

### New

* Add "When" step to allow skipping of tests depending on environment variable. [Ben Dalling]

### Changes

* Add details on upgrading from 1.X.X to 2.0.0. [Ben Dalling]

* Add the Snyk badge and reduce the size of the step functions. [Ben Dalling]

### Fix

* Refactor Markdown. [Ben Dalling]


## 1.0.6 (2022-07-18)

### Fix

* Correct code to work with pytest-bdd 6.0.1. [Ben Dalling]


## 1.0.5 (2022-07-17)

### Fix

* Fix the dynamic install requirements in setup.py. [Ben Dalling]


## 1.0.4 (2022-07-17)

### Fix

* Missing a comma in the version specifications for requirements. [Ben Dalling]


## 1.0.3 (2022-07-17)

### Fix

* Correct SemVer version for pytest-bdd requirement. [Ben Dalling]


## 1.0.2 (2022-07-17)

### Fix

* Correct the allowed range for pytest-bdd and pytest-testinfra (setup.py). [Ben Dalling]


## 1.0.1 (2022-07-17)

### Fix

* Temp disable of latest checks to cut a release. [Ben Dalling]

* Correct the allowed range for pytest-bdd and pytest-testinfra. [Ben Dalling]

* Reduce the size of testinfra_bdd/__init__.py. [Ben Dalling]


## 1.0.0 (2022-06-02)

### New

* Add address, port and socket checks. [Ben Dalling]

* Add process checks. [Ben Dalling]

* Add Pip package checks. [Ben Dalling]

### Fix

* Skip address and port tests on GitHub Actions as Azure blocks ICMP/Ping. [Ben Dalling]


## 0.3.0 (2022-06-01)

### New

* Allow the testing for a group properties. [Ben Dalling]


## 0.2.3 (2022-05-30)

### Fix

* Handle non-existent resources gracefully. [Ben Dalling]


## 0.2.2 (2022-05-23)

### Fix

* Ensure regex search in commount stream works. [Ben Dalling]


## 0.2.1 (2022-05-15)

### Fix

* Ensure install_requires has the required details in setup.py. [Ben Dalling]


## 0.2.0 (2022-05-14)

### New

* Add user checks to the fixtures. [Ben Dalling]

### Changes

* Correct minor typo. [Ben Dalling]


## 0.1.0 (2022-05-08)

### New

* Add checks for files. [Ben Dalling]

* Add checks for packages. [Ben Dalling]

* Add service checks. [Ben Dalling]

* Add documentation for the command and system info steps. [Ben Dalling]

* Implement fixtures from the host module. [Ben Dalling]

* Implement "When" Steps. [Ben Dalling]

* Add guidance on contributing. [Ben Dalling]

* Add code of conduct guidelines. [Ben Dalling]

* Implement "Given" Steps (fixes #1). [Ben Dalling]

### Fix

* Sort out YAML lint issues. [Ben Dalling]


## 0.0.2 (2022-05-02)

### Fix

* Correct release version. [Ben Dalling]


## 0.0.1 (2022-05-02)

### Changes

* Add CI status badge to the README.md file. [Ben Dalling]

### Fix

* Add missing requirements.txt file. [Ben Dalling]


## 0.0.0 (2022-05-02)

### New

* Add contents for a placeholder release. [Ben Dalling]

### Other

* Initial commit. [Ben Dalling]


