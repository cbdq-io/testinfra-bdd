Feature: Example of Testinfra BDD
  Give an example of all the possible Given, When and Then steps.

  Scenario: Start NTP Service
    Given the host with URL "docker://sut" is ready within 10 seconds
    When the command is "service ntp start"
    Then the command return code is 0

  Scenario: Test for Absent Resources
    Given the host with URL "docker://sut" is ready
    When the user is foo
    And the package is foo
    And the file is "/etc/foo.yml"
    Then the user state is absent
    And the package is absent
    And the file is absent

  Scenario: System Under Test
    Given the host with URL "docker://sut" is ready within 10 seconds
    When the system property type is not "linux" skip tests
    And the command is "ntpq -np"
    And the package is ntp
    And the file is /etc/ntp.conf
    And the user is "ntp"
    Then the command return code is 0
    And the command stdout contains "remote"
    And the package is installed
    And the file is present
    And the file type is file
    And the file owner is ntp
    And the file group is ntp
    And the file contents contains "debian.pool.ntp"
    And the file contents contains the regex ".*pool [0-9].debian.pool.ntp.org iburst"
    And the file mode is 0o544
    And the user state is present
    And the user group is ntp
    And the user uid is 101
    And the user gid is 101
    And the user home is /nonexistent
    And the user shell is /usr/sbin/nologin

  Scenario: Skip Tests if Host is Windoze
    Given the host with URL "docker://sut" is ready within 10 seconds
    When the system property type is not Windoze skip tests

  Scenario: Check Java is Installed in the Path
    Given the host with URL "docker://java11" is ready within 10 seconds
    Then the command "java" exists in path

  Scenario: Check Java 11 is Installed
    Given the host with URL "docker://java11" is ready
    When the command is "java -version"
    And the package is java-11-amazon-corretto-devel
    Then the command stderr contains "Corretto-11"
    And the command stderr contains the regex "openjdk version \"11\\W[0-9]"
    And the command stdout is empty
    And the command return code is 0
    And the package is installed

  Scenario Outline: Check a Service Status
    Given the host with URL "docker://sut" is ready
    When the service is <service_name>
    And the package is <package_name>
    And the file is <file_name>
    Then the service <status> enabled
    And the service <status> running
    And the package is <package_status>
    And the file is <file_status>
    Examples:
      | service_name | status | package_name | package_status | file_name       | file_status |
      | ntp          | is     | ntp          | installed      | /etc/ntp.conf   | present     |
      | named        | is not | named        | absent         | /etc/named.conf | absent      |
