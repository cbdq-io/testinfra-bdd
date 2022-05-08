Feature: Example of Testinfra BDD
  Give an example of all the possible Given, When and Then steps.

  Scenario: Start NTP Service
    Given the host with URL "docker://sut" is ready within 10 seconds
    When the command is "service ntp start"
    Then the command return code is 0

  Scenario: System Under Test
    Given the host with URL "docker://sut" is ready within 10 seconds
    When the system property type is not "linux" skip tests
    And the command is "ntpq -np"
    Then the command return code is 0
    And the command stdout contains "remote"

  Scenario: Skip Tests if Host is Windoze
    Given the host with URL "docker://sut" is ready within 10 seconds
    When the system property type is not Windoze skip tests

  Scenario: Check Java is Installed in the Path
    Given the host with URL "docker://java11" is ready within 10 seconds
    Then the command "java" exists in path

  Scenario: Check Java 11 is Installed
    Given the host with URL "docker://java11" is ready
    When the command is "java -version"
    Then the command stderr contains "Corretto-11"
    And the command stderr matches regex "openjdk version \"11\\W[0-9]"
    And the command stdout is empty
    And the command return code is 0
