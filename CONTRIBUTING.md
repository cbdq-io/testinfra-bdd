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
https://github.com/locp/testinfra-bdd/actions
