Feature: Tests Expected to Fail
  This is a collection of tests that are expected to fail.
  We a specifically testing functions within the Testinfra BDD module.

  Background: Specify a single false URL for a node that is not available.
    Given the Testinfra URL is docker://snafu

  Scenario: Host Not Available
    When host is ready

  Scenario: Host Not Available Within a Time
    When host is not ready within 2 seconds
