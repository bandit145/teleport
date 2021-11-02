import conn_track.utils as utils
import time
import sys

def read_file():
	with open('/proc/net/tcp', mode='r') as net_ncp:
		return net_ncp.read().strip().split('\n')

def run():
	try:
		# gather initial connections. We don't less these because we consider them existing
		connections = utils.parse_net_tcp(read_file())
		while True:
			time.sleep(10)
			cur_connections = utils.parse_net_tcp(read_file())
			new_conns = cur_connections.difference(connections)
			for conn in new_conns:
				connections.add(conn)
				print(f'New Connection: {conn.remote_address}:{conn.remote_port} -> {conn.local_address}:{conn.local_port}')
	except KeyboardInterrupt:
		print('User exited', file=sys.stderr)
		sys.exit(0)
