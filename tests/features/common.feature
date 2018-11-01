@common
Feature: Common samba tests

  @dns
  Scenario: Check that the resolv.conf was configured properly
    Given From any node in domain network
    When I run `host <domain.name>`
    Then It returns a list of domain controllers IPs
