Feature: Example of Testinfra BDD
  Give an example of all the possible Given, When and Then steps.

  The Given steps to skip the address and port tests when running under
  GitHub actions are not part of the testinfra-bdd package itself, but are
  required as GitHub/Azure does not allow Ping/ICMP traffic.

  Scenario: Skip Tests if Host is Windoze
    Given the TestInfra host with URL "docker://sut" is ready within 10 seconds
    # The system property can be one of:
    #   - type (e.g. linux).
    #   - distribution (e.g. debian).
    #   - release (e.g. 11).
    #   - codename (e.g. bullseye).
    #   - arch (e.g. x86_64).
    #   - hostname (e.g. sut).
    #   - connection_type (e.g. docker or ssh).
    When the TestInfra system property type is not Windoze skip tests

  Scenario Outline: Test for Absent Resources
    Given the TestInfra host with URL "docker://sut" is ready within 10 seconds
    When the TestInfra <resource_type> is "foo"
    Then the TestInfra <resource_type> is absent
    Examples:
      | resource_type |
      | user          |
      | group         |
      | package       |
      | file          |
      | pip package   |

  Scenario Outline: Test for Absent Non-Quoted Resources
    # Same as the example above except the resources are not quoted.
    Given the TestInfra host with URL "docker://sut" is ready within 10 seconds
    When the TestInfra <resource_type> is foo
    Then the TestInfra <resource_type> state is absent
    Examples:
      | resource_type |
      | user          |
      | group         |
      | package       |
      | file          |
      | pip package   |

  Scenario: User Checks
    Given the TestInfra host with URL "docker://sut" is ready
    When the TestInfra user is "ntp"
    Then the TestInfra user is present
    # Alternative method of checking the state of a resource.
    And the TestInfra user state is present
    And the TestInfra user group is ntp
    And the TestInfra user uid is 101
    And the TestInfra user gid is 101
    And the TestInfra user home is /nonexistent
    And the TestInfra user shell is /usr/sbin/nologin

  Scenario: File Checks
    Given the TestInfra host with URL "docker://sut" is ready
    When the TestInfra file is /etc/ntp.conf
    # Expected state can be present or absent.
    Then the TestInfra file is present
    # Alternative method of checking the state of a resource.
    And the TestInfra file state is present
    # Valid types to check for are file, directory, pipe, socket or symlink.
    And the TestInfra file type is file
    And the TestInfra file owner is ntp
    And the TestInfra file group is ntp
    And the TestInfra file contents contains "debian.pool.ntp"
    And the TestInfra file contents contains the regex ".*pool [0-9].debian.pool.ntp.org iburst"
    # The expected mode must be specified as an octal.
    And the TestInfra file mode is 0o544

  Scenario: File Executable Checks
    Given the TestInfra host with URL "docker://sut" is ready
    When the TestInfra file is /bin/ls
    Then the TestInfra file is present
    And the TestInfra file is executable

  Scenario: Group Checks
    Given the TestInfra host with URL "docker://sut" is ready
    When the TestInfra group is "ntp"
    # Can check if the group is present or absent.
    Then the TestInfra group is present
    # Alternative method of checking the state of a resource.
    And the TestInfra group state is present
    And the TestInfra group gid is 101

  Scenario: Group Membership
    Given the TestInfra host with URL "docker://sut" is ready
    When the TestInfra group is "sudo"
    And the TestInfra user is "bar"
    Then the TestInfra group contains the user "bar"
    And the TestInfra user groups include "sudo"

  Scenario: Running Commands
    Given the TestInfra host with URL "docker://sut" is ready
    When the TestInfra command is "ntpq -np"
    Then the TestInfra command return code is 0
    And the TestInfra command "ntpq" exists in path
    And the TestInfra command stdout contains "remote"
    And the TestInfra command stdout does not contain "foo"

  Scenario: System Package
    Given the TestInfra host with URL "docker://sut" is ready
    When the TestInfra package is ntp
    # Can check if the package is absent, present or installed.
    Then the TestInfra package is installed
    And the TestInfra package version will be greater than or equal to 1:4.2.8p15+dfsg-1

  Scenario: Python Package
    Given the TestInfra host with URL "docker://sut" is ready
    When the TestInfra pip package is testinfra-bdd
    # Can check if the package is absent or present.
    Then the TestInfra pip package is present
    And the TestInfra pip package version is 3.1.1
    And the TestInfra pip package version will be greater than or equal to 3.0.5
    # Check that installed packages have compatible dependencies.
    And the TestInfra pip check is OK

  Scenario Outline: Service Checks
    Given the TestInfra host with URL "docker://sut" is ready
    When the TestInfra service is <service>
    Then the TestInfra service is <running_state>
    And the TestInfra service is <enabled_state>
    Examples:
      | service | running_state | enabled_state |
      | ntp     | running       | enabled       |
      | named   | not running   | not enabled   |

  Scenario: Test Running Processes
    Given the TestInfra host with URL "docker://sut" is ready
    # Processes are selected using filter() attributes names are
    # described in the ps man page.
    When the TestInfra process filter is "user=root,comm=ntpd"
    Then the TestInfra process count is 1

  Scenario Outline: Test Pip Packages are Latest Versions
    Given the TestInfra host with URL "docker://sut" is ready
    When the TestInfra pip package is <pip_package>
    Then the TestInfra pip package is present
    And the TestInfra pip package is <status>
    Examples:
      | pip_package      | status |
      | pytest-bdd       | latest |
      | pytest-testinfra | latest |
      | testinfra-bdd    | latest |

  Scenario Outline:  Check Sockets
    # This checks that NTP is listening but SSH isn't.
    # The socket url is defined at https://testinfra.readthedocs.io/en/latest/modules.html#socket
    Given the TestInfra host with URL "docker://sut" is ready within 10 seconds
    When the TestInfra socket is <url>
    Then the TestInfra socket is <expected_state>
    Examples:
      | url       | expected_state |
      | udp://123 | listening      |
      | tcp://22  | not listening  |

  Scenario: Skip Tests Due to Environment Variable
    Given the TestInfra host with URL "docker://java11" is ready
    When the TestInfra environment variable PYTHONPATH is .:.. skip tests

  Scenario: Check Network Address
    Given the TestInfra host with URL "docker://sut" is ready within 10 seconds
    When the TestInfra environment variable GITHUB_ACTIONS is true skip tests
    And the TestInfra address is www.google.com
    Then the TestInfra address is resolvable
    And the TestInfra address is reachable

  Scenario: Check Network Address With Port
    Given the TestInfra host with URL "docker://sut" is ready within 10 seconds
    When the TestInfra environment variable GITHUB_ACTIONS is true skip tests
    And the TestInfra address and port is www.google.com:443
    Then the TestInfra address is resolvable
    And the TestInfra address is reachable
    And the TestInfra port is reachable

  Scenario: Check Java is Installed in the Path
    Given the TestInfra host with URL "docker://java11" is ready within 10 seconds
    Then the TestInfra command "java" exists in path

  Scenario: Check Java 11 is Installed
    Given the TestInfra host with URL "docker://java11" is ready
    When the TestInfra command is "java -version"
    And the TestInfra package is java-11-amazon-corretto-devel
    Then the TestInfra command stderr contains "Corretto-11"
    And the TestInfra command stderr contains the regex "openjdk version \"11\\W[0-9]"
    And the TestInfra command stdout is empty
    And the TestInfra command return code is 0
    And the TestInfra package is installed

  Scenario: Check for an Expected Value
   # In this example we set the expected_value to "foo"
   Given the TestInfra host with URL "docker://sut" is ready
   And the TestInfra expected value is "foo"
   When the TestInfra command is "echo foo"
   Then the TestInfra command stdout contains the expected value

  Scenario Outline: Check Contents of JSON File With JMESPath
    Given the TestInfra host with URL "docker://sut" is ready
    When the TestInfra file is /tmp/john-smith.json
    Then the TestInfra JMESPath expression <expression> returns <expected_value>
    Examples:
      | expression    | expected_value |
      | firstName     | John           |
      | lastName      | Smith          |
      | age           | 27             |
      | address.state | NY             |
      | spouse        | None           |
