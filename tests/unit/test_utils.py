import conn_track.utils as utils
from conn_track.classes import Connection

net_tcp_test_data = '''sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode
 0: 00000000:1F99 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 30876 1 0000000000000000 100 0 0 10 0
 1: 00000000:DFF9 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 22564 1 0000000000000000 100 0 0 10 0
 2: 00000000:BDDB 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 22572 1 0000000000000000 100 0 0 10 0
 3: 00000000:0801 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 15863 1 0000000000000000 100 0 0 10 0
 4: 0100007F:8287 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 26899 1 0000000000000000 100 0 0 10 0
 5: 00000000:98CB 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 15877 1 0000000000000000 100 0 0 10 0
 6: 00000000:006F 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 19457 1 0000000000000000 100 0 0 10 0
 7: 00000000:B315 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 22580 1 0000000000000000 100 0 0 10 0
 8: 3500007F:0035 00000000:0000 0A 00000000:00000000 00:00000000 00000000   102        0 11914 1 0000000000000000 100 0 0 10 0
 9: 00000000:0016 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 26856 1 0000000000000000 100 0 0 10 0
10: E10FA20A:8CF8 0F5BBD5B:0050 06 00000000:00000000 03:00001212 00000000     0        0 0 3 0000000000000000
11: E10FA20A:CCA0 6E0DD9AC:0050 06 00000000:00000000 03:00001211 00000000     0        0 0 3 0000000000000000
12: E10FA20A:DC1A FEA9FEA9:0050 01 00000000:00000000 00:00000000 00000000     0        0 25370 1 0000000000000000 20 0 0 10 -1
13: E10FA20A:DC1E FEA9FEA9:0050 01 00000000:00000000 00:00000000 00000000     0        0 28696 1 0000000000000000 20 0 0 10 -1
14: E10FA20A:D8B4 9858BD5B:0050 06 00000000:00000000 03:00001219 00000000     0        0 0 3 0000000000000000
15: E10FA20A:AD6C 145CBD5B:01BB 01 00000000:00000000 00:00000000 00000000     0        0 27228 1 0000000000000000 28 4 23 10 -1
16: E10FA20A:DC1C FEA9FEA9:0050 01 00000000:00000000 00:00000000 00000000     0        0 27744 1 0000000000000000 20 0 0 10 -1
17: E10FA20A: 2A5BBD5B:01BB 01 00000000:00000000 00:00000000 00000000     0        0 28072 1 0000000000000000 21 4 0 10 -1
18: E10FA20A:0016 3BD7E1CC:D94B 01 00000000:00000000 02:000AF7F9 00000000     0        0 27208 3 0000000000000000 22 4 29 10 -1
19: E10FA20A:E6A6 B358BD5B:01BB 01 00000000:00000000 00:00000000 00000000     0        0 26165 1 0000000000000000 28 4 0 10 -1
20: E10FA20A:D8B2 9858BD5B:0050 06 00000000:00000000 03:00001219 00000000     0        0 0 3 0000000000000000
'''

def test_little_to_big_endian():
	# E10FA20A == 10.162.15.225
	assert utils.little_to_big_endian('E10FA20A') == '0AA20FE1'
	assert utils.little_to_big_endian('0100007F') == '7F000001'

def test_parse_net_tcp():
	connections = utils.parse_net_tcp(net_tcp_test_data.strip().split('\n'))
	print(connections)
	len(connections) == 11
	assert Connection('169.254.169.254', 80, '10.162.15.225', 56348, None) in connections
	assert Connection('91.189.91.42', 443, '10.162.15.225', None, None) in connections
