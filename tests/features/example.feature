Feature: Example of Testinfra BDD
  Give an example of the possible Given, When and Then steps.

  Scenario: System Under Test
    Given Testinfra URL is docker://sut
    When Testinfra host is ready within 10 seconds
    And Testinfra host is ready
    And Testinfra host type is linux or skip tests
    And Testinfra host distribution is debian or skip tests
    And Testinfra host release is 11 or skip tests
    And Testinfra host codename is bullseye or skip tests
    And Testinfra host arch is x86_64 or skip tests
