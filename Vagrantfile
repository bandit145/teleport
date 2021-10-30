Vagrant.configure("2") do |config|

        (1..2).each do |i|
                config.vm.define "server#{i}" do |client|
                        client.vm.box = "bento/ubuntu-20.04"
			client.vm.provider "virtualbox" do |vm|
				vm.memory = 2048
                                vm.cpus = 1
			end

			client.vm.provision "shell", inline: "add-apt-repository ppa:deadsnakes/ppa && apt-get update && apt-get install -y python3.10 python3-minimal python3-pip"
               end
        end

end

