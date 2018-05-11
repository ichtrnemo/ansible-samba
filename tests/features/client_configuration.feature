Feature: Node is configured as a domain client

  Scenario: Kerberos functionality
    Given As a member of <domain.name> domain
    When I run `kinit <username@domain.name>`
    Then it returns a kerberos ticket
