Feature: Lines of Code
  Scenario Outline: Check Lines of Code in Radon Report
    Given a Radon report
    When Python source file is file
    Then lines of code must not be greater than <max_lines_of_code>
    Examples:
      | max_lines_of_code |
      | 250               |
