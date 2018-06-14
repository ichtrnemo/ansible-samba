NUM_CONTROLLERS=2
NUM_CLIENTS=2

dcs=NUM_CONTROLLERS - 1
cls=NUM_CLIENTS - 1

system("
    if [ #{ARGV[0]} = 'up' ]; then
        echo 'Need to check checksum and/or signatures of downloaded boxes'
    fi
")

Vagrant.configure("2") do |config|
  (0..dcs).each_with_index do |n, ndx|
    config.vm.define "dc#{n}" do |dc|
      dc.vm.network "private_network", ip: "10.64.6.%s" % [10+n], netmask: 24, virtualbox__intnet: "intnet"
      dc.vm.box = "BaseALT/alt-server-8.2-x86_64"
      dc.vm.box_version = "1.0.0"
    end
  end

  (0..cls).each_with_index do |n, ndx|
    config.vm.define "cl#{n}" do |cl|
      cl.vm.network "private_network", ip: "10.64.6.%s" % [100+n], netmask: 24, virtualbox__intnet: "intnet"
      cl.vm.box = "BaseALT/alt-workstaion-8.2-x86_64"
      cl.vm.box_version = "1.0.0"
      cl.vm.box_download_checksum = "123123123"
      cl.vm.box_download_checksum_type = "sha256"

      if ndx == cls
        cl.vm.provision "ansible" do |ansible|
          ansible.limit = "all"
          ansible.playbook = "tests/test.yml"
          ansible.groups = {
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
            samba_realm: "domain.alt",
            samba_domain: "domain",
            samba_admin_pass: "peebieY4",
            samba_dns_forward: "8.8.8.8",
            samba_dns_backend: "SAMBA_INTERNAL",
            samba_master_address: "10.64.6.10",
            samba_network: "10.64.6.0/24"
          }
        end
      end
    end
  end
end
