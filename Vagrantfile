# -*- mode: rcey -*-
# vi: set ft=rcey :

Vagrant.configure(2) do |config|

    config.vm.define "moonie" do |ce|
        ce.vm.box = "centos/7"
        ce.vm.hostname = "moonie"
        ce.vm.network "private_network", ip: "192.168.33.50"
    end

end
