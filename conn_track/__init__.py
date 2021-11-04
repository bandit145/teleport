import conn_track.utils as utils
import time
import sys
from prometheus_client import Counter, start_http_server

def read_file():
	with open('/proc/net/tcp', mode='r') as net_ncp:
		return net_ncp.read().strip().split('\n')

def process_connections(new_conns, connections, conn_counter):
	for conn in new_conns:
		conn_counter.inc()
		connections.add(conn)
		if conn.direction == 'inbound':
			print(f'New Connection:  {conn.local_address}:{conn.local_port} <- {conn.remote_address}:{conn.remote_port}')
		elif conn.direction == 'outbound':
			print(f'New Connection:  {conn.local_address}:{conn.local_port} -> {conn.remote_address}:{conn.remote_port}')

def run():
	try:
		# gather initial connections. We don't less these because we consider them existing
		connections = utils.parse_net_tcp(read_file())
		conn_counter = Counter('new_connections', 'Number of new connections')
		start_http_server(9000)
		while True:
			time.sleep(10)
			connections = utils.purge_old_conns(connections)
			cur_connections = utils.parse_net_tcp(read_file())
			new_conns = cur_connections.difference(connections)
			print(new_conns)
			process_connections(new_conns, connections, conn_counter)
			utils.block_addresses(utils.generate_block_list(connections))
	except KeyboardInterrupt:
		print('User exited', file=sys.stderr)
		sys.exit(0)
