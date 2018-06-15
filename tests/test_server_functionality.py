# coding=utf-8
"""Domain controllers feature tests."""

from pytest_bdd import (
    given,
    scenario,
    then,
    when,
)
from conftest import assert_cmd
import pytest

@scenario('features/server_functionality.feature', 'Each domain controller can see each other')
def test_each_domain_controller_can_see_each_other(ssh_dcs, dcs):
    """Each domain controller can see each other."""
    pass


@given('From any domain controller')
def from_any_domain_controller():
    """From any domain controller."""


@when('I ping other controllers')
def i_ping_other_controllers(ssh_dcs, dcs):
    """I ping other controllers."""
    ssh_dcs.exec_command('ping -c1 -w1 {}'.format(dcs))


@then('They reply to ping request')
def they_reply_to_ping_request(ssh_dcs):
    """They reply to ping request."""
    assert ssh_dcs.res['rc'] == 0, "[{}]: {} failed.".format(ssh_dcs.host, ssh_dcs.res['cmd'])


@scenario('features/server_functionality.feature', 'Users list')
def test_users_list(ssh_dcs):
    """Users list."""
    pass


@when('I try to get users list')
def i_try_to_get_users_list(ssh_dcs):
    """I try to get users list."""
#    expect = lambda res: res['rc'] == 0 and len(res['stdout']) > 0 and 'Administrator' in res['stdout']
#    assert_cmd(expect, ssh_dcs.exec_command('samba-tool user list'))
    ssh_dcs.exec_command('sudo samba-tool user list')


@then('It returns non empty list that contains Administrator user')
def it_returns_non_empty_list_that_contains_administrator_user(ssh_dcs):
    """It returns non empty list that contains Administrator user."""
    res = ssh_dcs.res
    assert res['rc'] == 0
    assert len(res['stdout']) > 0
    assert 'Administrator' in res['stdout'].split('\n')
