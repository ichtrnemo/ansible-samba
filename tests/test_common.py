# coding=utf-8
"""Common samba tests feature tests."""

from pytest_bdd import (
    given,
    scenario,
    then,
    when,
)
import pytest
from conftest import assert_cmd

@scenario('features/common.feature', 'Check that the resolv.conf was configured properly')
def test_check_that_the_resolvconf_was_configured_properly(ssh_all):
    """Check that the resolv.conf was configured properly."""

@given('From any node in domain network')
def from_any_node_in_domain_network(ssh_all):
    res = ssh_all.exec_command('hostname')
    """From any node in domain network."""


@when('I run `host <domain.name>`')
def i_run_host_domainname(ssh_all, samba_params):
    """I run `host <domain.name>`."""
    expect = lambda res: res['rc'] == 0 and len(res['stdout']) > 0
    assert_cmd(expect, ssh_all.exec_command('host {}'.format(samba_params['realm'])))


@then('It returns a list of domain controllers IPs')
def it_returns_a_list_of_domain_controllers_ips():
    """It returns a list of domain controllers IPs."""
