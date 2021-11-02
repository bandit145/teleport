import ipaddress
import time
from conn_track.classes import Connection

#need to ignore client outbound connections
def parse_net_tcp(net_tcp):
	conn_list = set()
	# remove headers
	del net_tcp[0]
	for line in net_tcp:
		line = line.split()
		#print(line)
		local_address, local_port  = parse_address(line[1])
		remote_address, remote_port  = parse_address(line[2])
		state = int(line[3], base=16)
		# unsure what these connections are but they don't appear to be valid since the remote address is 0.0.0.0:0
		if state != 10:
			#conn_list.append({'local_address': local_address, 'local_port': local_port, 'remote_address': remote_address, 'remote_port': remote_port})
			conn_list.add(Connection(remote_address, remote_port, local_address, local_port, time.time()))
			# if remote_address in conn_list.keys():
			# 	conn_list[remote_address][remote_port] = {'local_port': local_port, 'local_address': local_address, 'time': time.time()}
			# else:
			# 	conn_list[remote_address] = {remote_port: {'local_port': local_port, 'local_address': local_address, 'time': time.time()}}
	return conn_list

def little_to_big_endian(hex_str):
	lit_hex = ''
	for num in range(len(hex_str) -2, -2, -2):
		lit_hex += hex_str[num] + hex_str[num+1]
	return lit_hex

def parse_address(address):
	address, port = address.split(':')
	address = str(ipaddress.ip_address(int(little_to_big_endian(address), base=16)))
	# port numbers are big endian
	if port != '':
		port  = int(port, base=16)
	else:
		port = None
	return address, port