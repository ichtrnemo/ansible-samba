require 'mkmf'
require 'fileutils'

NUM_CONTROLLERS=3
NUM_CLIENTS=3

dcs=NUM_CONTROLLERS - 1
cls=NUM_CLIENTS - 1

if ARGV[0] == 'up' or ARGV[0] == 'provision'
  if not find_executable 'ansible-playbook'
    raise "ansible-playbook was not found in your PATH"
  end
end

Vagrant.configure("2") do |config|
  config.vbguest.auto_update = false

  (0..dcs).each_with_index do |n, ndx|
    config.vm.define "dc#{n}" do |dc|

      dc.vm.network "private_network", ip: "10.64.6.%s" % [10+n], netmask: 24, virtualbox__intnet: "intnet"
      dc.vm.box = "BaseALT/alt-server-9.2-amd64"
      dc.vm.box_version = "1.0.0"

    end
  end

  (0..cls).each_with_index do |n, ndx|
    config.vm.define "cl#{n}" do |cl|
      cl.vm.network "private_network", ip: "10.64.6.%s" % [100+n], netmask: 24, virtualbox__intnet: "intnet"
      cl.vm.box = "BaseALT/alt-workstation-9.2-amd64"
      cl.vm.box_version = "1.0.0"

      if ndx == cls
        cl.vm.provision "ansible" do |ansible|
          ansible.compatibility_mode = "2.0"
          ansible.become_user = "root"
          ansible.limit = "all"
          ansible.playbook = "provision.yml"
          ansible.groups = {
            "all:vars" => {
              "ansible_become" => "yes"
            },
            "sambaDC-master" => ["dc0"],
            "sambaDC-master:vars" => {
              "samba_flavor" => "master"
            },
            "sambaDC-replicas" => (1..dcs).map {|x| "dc#{x}"},
            "sambaDC-replicas:vars" => {
              "samba_flavor" => "replica"
            },
            "samba-clients" => (0..cls).map {|x| "cl#{x}"},
            "samba-clients:vars" => {
              "samba_flavor" => "client"
            },
          }
          ansible.extra_vars = {
            ansible_python_interpreter: "/usr/bin/python3",
            samba_realm: "domain.alt",
            samba_domain: "domain",
            samba_admin_pass: "peebieY4",
            samba_dns_forward: "8.8.8.8",
            samba_dns_backend: "BIND9_DLZ",
            samba_backend_store: "mdb",
            samba_dc_mitkrb5: true,
            samba_master_address: "10.64.6.10",
            samba_network: "10.64.6.0/24",
            samba_generate_domain_config: true,
            samba_domain_config_output: "domain_config",
            gen_test_env: true
          }
        end
      end
    end
  end
end

if ARGV[0] == 'up' or ARGV[0] == 'provision'
# generate environment files for pytest
  FileUtils::mkdir_p '.tmp'
  File.open(".tmp/domain_config", "w") { |f|
    f << "export SAMBA_DOMAIN=domain\n"
    f << "export SAMBA_REALM=domain.alt\n"
    f << "export SAMBA_ADMIN_PASS=peebieY4\n"
    f << "export SAMBA_MASTER_ADDRESS=10.64.6.1\n"
    f << "export SAMBA_MASTER_HOSTNAME=dc0\n"
    f << "export SAMBA_MASTERS=\"dc0\"\n"
    f << "export SAMBA_REPLICAS=\"#{(1..dcs).map {|x| "dc#{x}"}.join(' ')}\"\n"
    f << "export SAMBA_CLIENTS=\"#{(0..cls).map {|x| "cl#{x}"}.join(' ')}\"\n"
  }
end
