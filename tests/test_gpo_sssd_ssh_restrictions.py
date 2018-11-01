# coding=utf-8
"""SSSD GPO ssh restrictions feature tests."""

from pytest_bdd import (
    given,
    scenario,
    then,
    when,
)
#import pytest
#from conftest import assert_cmd

@scenario('features/gpo_sssd_ssh_restrictions.feature', 'User`s access should be restricted by sssd')
def test_users_access_should_be_restricted_by_sssd(ssh_ms):
    """User`s access should be restricted by sssd."""


@given('a <user> with <password>')
def params(ssh_ms, user, password):
    """a <user> with <password>."""
    return dict(user=user,password=password,rc=None)


@when('ssh from domain master to <dest> and execute of <command>')
def ssh_command(ssh_ms, params, dest, command):
    """ssh from <src> to <dest> and execute of <command>."""
    res = ssh_ms.exec_command('sshpass -p %s ssh %s@%s %s' % (params['password'], params['user'], dest, command))
    params['rc'] = res['rc']


@then('the exit code should be <rc>')
def the_exit_code_should_be_rc(params, rc):
    """the exit code should be <rc>."""
    assert params['rc'] == int(rc)
