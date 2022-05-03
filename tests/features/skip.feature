Feature: Test Scenarios That Might Allow Tests to be Skipped
  Scenario Outline: Skip Tests on Non-Existent Host
    Given Testinfra URL is <url>
    When Testinfra host is ready or skip tests
    Then raise NotImplementedError
    Examples:
      | url          |
      | docker://foo |

  Scenario Outline: Skip Tests on Non-Existent Host After Waiting
    Given Testinfra URL is <url>
    When Testinfra host is ready within <seconds> seconds or skip tests
    Then raise NotImplementedError
    Examples:
      | url          | seconds |
      | docker://foo | 2       |

  Scenario: Skip Tests Due to Arch
    Given Testinfra URL is docker://sut
    When Testinfra host is ready within 10 seconds
    And Testinfra host arch is foo or skip tests
    Then raise NotImplementedError

  Scenario: Skip Tests Due to Codename
    Given Testinfra URL is docker://sut
    When Testinfra host is ready within 10 seconds
    And Testinfra host codename is foo or skip tests
    Then raise NotImplementedError

  Scenario: Skip Tests Due to Distribution
    Given Testinfra URL is docker://sut
    When Testinfra host is ready within 10 seconds
    And Testinfra host distribution is foo or skip tests
    Then raise NotImplementedError

  Scenario: Skip Tests Due to Release
    Given Testinfra URL is docker://sut
    When Testinfra host is ready within 10 seconds
    And Testinfra host release is 42 or skip tests
    Then raise NotImplementedError

  Scenario: Skip Tests Due to Type
    Given Testinfra URL is docker://sut
    When Testinfra host is ready within 10 seconds
    And Testinfra host type is Windoze or skip tests
    Then raise NotImplementedError
