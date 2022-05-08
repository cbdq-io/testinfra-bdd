Feature: Test the utility functions
  Scenario Outline: Test Get Host from Fixture
    Given JSON text is "<json_text>"
    When text is passed as a dict to get_resource_from_fixture
    Then expect "<exception_message>" as a ValueError
    Examples:
      | json_text                     | exception_message                                        |
      | {}                            | Badly constructed test fixture.  Missing the host "url". |
      | {"url": "foo"}                | Badly constructed test fixture.  Missing the "host".     |
      | {"url": "foo", "host": "foo"} | Resource "foo" not found.  Did you miss a "When" step?   |

  Scenario: Expect Unready Host
    Given a host specification of "docker://foo"
    Then expect the host to be unready

  Scenario Outline: Get System Properties
    Given a host specification of "local://"
    When "<property_name>" is requested from the host
    Then status should be <status>
    Examples:
      | property_name | status |
      | type          | OK     |
      | foo           | NOK    |

  Scenario: Request for Invalid Resource Should Fail
    Given the host with URL "docker://sut" is ready
    When a resource called "foo" is requested
    Then the ValueError exception will be 'Unknown resource type "foo".'

  Scenario: Unknown stream name for a command
    Given the host with URL "docker://sut" is ready
    When the command is "java -version"
    Then expect an exception from stream name of "foo"
