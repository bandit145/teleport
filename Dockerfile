FROM docker.io/ubuntu
RUN apt-get update -y
EXPOSE 9000
RUN apt-get install -y iptables python3-minimal python3-pip
COPY . /conn-track
RUN pip3 install /conn-track
ENTRYPOINT ["conn-track"]