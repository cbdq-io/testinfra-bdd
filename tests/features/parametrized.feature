Feature: parametrized
    Scenario: Parametrized URL
        Given the Testinfra URL parameter is url
        When Testinfra host is ready within 10 seconds
        And Testinfra host is ready
