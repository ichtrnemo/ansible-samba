"""Configuration for pytest runner."""

from pytest_bdd import given, when
import pytest
import paramiko
from paramiko.config import SSHConfig
from os.path import expanduser
import sys
import os
import inspect

pytest_plugins = "pytester"
samba = {}

SSH_USERNAME = os.getenv("SSH_USERNAME", "vagrant")

class Target:
    def __init__(self, host):
        self.host = host
        config_file = file(expanduser('.tmp/ssh_config'))
        config = SSHConfig()
        config.parse(config_file)
        ip = config.lookup(host).get('hostname', None)
        port = config.lookup(host).get('port', 22)
        pk = config.lookup(host).get('identityfile', None)

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=ip, port=int(port), username=SSH_USERNAME, key_filename=pk)

    def __exit__(self):
        self.ssh.close()

    def exec_command(self, cmd):
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(cmd)
        self.res =  {'rc': ssh_stdout.channel.recv_exit_status(),
                     'cmd': cmd,
                     'host': self.host,
                     'stdout': ssh_stdout.read(),
                     'stderr': ssh_stderr.read()}
        return self.res


@given("I have a root fixture")
def root():
    return "root"


@when("I use a when step from the parent conftest")
def global_when():
    pass


def assert_cmd(expect, res):
    assert expect(res), "execution of '{}' failed on '{}' with '{}'; lambda is: {}".format(res['cmd'], res['host'], res['stdout'] + res['stderr'], inspect.getsource(expect))


def read_env_vars():
    req_vars = ['SAMBA_DOMAIN',
                'SAMBA_REALM',
                'SAMBA_ADMIN_PASS',
                'SAMBA_MASTER_ADDRESS',
                'SAMBA_MASTER_HOSTNAME',
                'SAMBA_MASTERS',
                'SAMBA_REPLICAS',
                'SAMBA_CLIENTS']
    list_vars = ['SAMBA_MASTERS',
                'SAMBA_REPLICAS',
                'SAMBA_CLIENTS']

    for v in req_vars:
        if v not in os.environ:
            print('{} required but is not set'.format(v))
            sys.exit(1)
        samba[v.split('_',1)[1].lower()] = os.environ[v] if v not in list_vars else filter(None, os.environ[v].split(' '))
    samba['all_hosts'] = samba['masters'] + samba['replicas'] + samba['clients']
read_env_vars()

@pytest.fixture(scope='session', params=samba['all_hosts'])
def ssh_all(request):
    return Target(request.param)

@pytest.fixture(scope='session', params=samba['masters'])
def ssh_ms(request):
    return Target(request.param)

@pytest.fixture(scope='session', params=samba['replicas'])
def ssh_rs(request):
    return Target(request.param)

@pytest.fixture(scope='session', params=samba['masters'] + samba['replicas'])
def ssh_dcs(request):
    return Target(request.param)

@pytest.fixture(scope='session', params=samba['clients'])
def ssh_cs(request):
    return Target(request.param)

@pytest.fixture(scope='session', params=samba['masters'] + samba['replicas'])
def dcs(request):
    return request.param

@pytest.fixture(scope='session')
def samba_params():
    return samba
