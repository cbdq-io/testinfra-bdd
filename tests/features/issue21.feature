Feature: Fix Issue 21
  See https://github.com/cbdq-io/testinfra-bdd/issues/21

  Scenario: Issue 21
    Given the TestInfra host with URL "docker://sut" is ready within 10 seconds
    When the TestInfra command is "cat /tmp/issue21.txt"
    Then the TestInfra command stdout contains "Datacenter: DC1"
    And the TestInfra command stdout contains the regex "UN.*RACK1"
