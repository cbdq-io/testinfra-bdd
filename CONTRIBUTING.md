# Contributing to Testinfra BDD

This project is developed using a standard Github pull request
process. Almost all code is reviewed in pull requests.

The general process for working on ansible-role-cassandra is:

- Fork the project on Github
- Clone your fork to your local machine
- Create a feature branch from `develop` (e.g.
  `git branch delete_all_the_code`)
- Write code, commit often
- Write test cases for all changed functionality
- Submit a pull request against `develop` on Github
- Wait for code review!

Things that will make your branch more likely to be pulled:

- Comprehensive, fast test cases
- Detailed explanation of what the change is and how it works
- Reference relevant issue numbers in the tracker
- API backward compatibility

## Testing

Tests are run against a branch pushes and pull requests using GitHub
Workflows for this project these are visible at
<https://github.com/locp/testinfra-bdd/actions>

## Cutting a Release

Ensure your local repo is up-to-date:

```shell
git checkout develop
git fetch -p origin && git pull && git pull --tags
git checkout main
git pull
```

Now set a shell variable to help us create the release:

```shell
RELEASE='0.1.0'
git flow release start $RELEASE
```

Now edit `testinfra_bdd/__init__.py` and ensure that the `__version__`
variable is set to the same value as `$RELEASE`.

Now update the `CHANGELOG.md` with:

```shell
make changelog
```

Now commit these changes in a way that we don't have excessive messages
in the changelog:

```shell
git add .
git commit -m "chg: doc: Release ${RELEASE} \!minor"
```

Now finish the release in Git Flow:

```shell
git flow finish -m "v${RELEASE}" -p
```

When all the CI jobs have completed, create the new release at
<https://github.com/locp/testinfra-bdd/releases>

### Post Release Steps

After a release has been published, ensure the testinfra-bdd Python
package has been updated in `tests/features/example.feature` for the
tests to continue working.
