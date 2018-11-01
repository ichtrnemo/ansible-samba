@sssd
Feature: SSSD GPO ssh restrictions
  SSSD should restict user access according to GPO configuration

  Scenario Outline: User`s access should be restricted by sssd
    Given a <user> with <password>
    When ssh from domain master to <dest> and execute of <command>
    Then the exit code should be <rc>

    Examples:
    | user      | password     | dest | command   |  rc |
    | adgpotest | ADgpoTest123 | cl0  | /bin/true |   0 |
    | adgpotest | ADgpoTest123 | clw0 | /bin/true | 255 |
    | adgpotest | ADgpoTest123 | clw1 | /bin/true | 255 |
