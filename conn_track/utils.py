import ipaddress
import time
import subprocess
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
		direction = None
		# shortcut: Checking the if it's a highnumber connection to a reserved port or vise versa should cover like >90% of directionality cases.
		if remote_port >= 1024 and local_port < 1024:
			direction = 'inbound'
		elif local_port >= 1024 and remote_port < 1024:
			direction = 'outbound'
		elif local_port < 1024:
			direction = 'inbound'

		# ignore listening sockets
		if state != 10:
			conn_list.add(Connection(remote_address, remote_port, local_address, local_port, time.time(), direction))
	return conn_list

def little_to_big_endian(hex_str):
	lit_hex = ''
	for num in range(len(hex_str) -2, -2, -2):
		lit_hex += hex_str[num] + hex_str[num+1]
	return lit_hex

# is this efficent? Hell no, but it'll work for now. I'd have to look into redoing the initial datastrucure if I wanted to avoid all this extra looping I think.
def generate_block_list(conn_list):
	block_cnt = {}
	block_list = []
	for conn in conn_list:
		if conn.direction == 'inbound':
			if conn.remote_address in block_cnt.keys():
				#this if it is the same port duplicates will not be allowed in the set
				block_cnt[conn.remote_address]['ports'].add(conn.local_port)
				block_cnt[conn.remote_address]['local_addr'] = conn.local_address
			else:
				block_cnt[conn.remote_address] = {'ports': set([conn.local_port]), 'local_address': conn.local_address}
	print(block_cnt)
	for item, value in block_cnt.items():
		if len(value['ports']) >= 3:
			block_list.append(item)
			print('Port scan detected:', item, '->', value["local_address"], 'on ports', ','.join([str(x) for x in value["ports"]]))
	return block_list

# this funciton is for pruning connections so we don't build up a massive list and so we know everything we are checking against for block is < 90 seconds old.
def purge_old_conns(conn_list):
	new_conns = set()
	cur_time = time.time()
	for conn in conn_list:
		if cur_time - conn.time < 60:
			new_conns.add(conn)
		else:
			print('purging connection!')
	return new_conns

def parse_address(address):
	address, port = address.split(':')
	address = str(ipaddress.ip_address(int(little_to_big_endian(address), base=16)))
	# port numbers are big endian
	if port != '':
		port  = int(port, base=16)
	else:
		port = 0
	return address, port

def block_addresses(addr_list):
	for addr in addr_list:
		subprocess.run(['iptables', '-|', 'INPUT', '-s', addr, '-j', 'DROP'])