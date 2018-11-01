@basic
Feature: Node is configured as a domain client

  @kerberos
  Scenario: Kerberos functionality
    Given As a member of <domain.name> domain
    When I run `kinit <username@domain.name>`
    Then it returns a kerberos ticket
