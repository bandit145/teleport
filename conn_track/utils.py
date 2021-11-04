import ipaddress
import time
import subprocess
from conn_track.classes import Connection

# need to ignore client outbound connections
def parse_net_tcp(net_tcp):
    conn_list = set()
    # remove headers
    del net_tcp[0]
    for line in net_tcp:
        line = line.split()
        # print(line)
        local_address, local_port = parse_address(line[1])
        remote_address, remote_port = parse_address(line[2])
        state = int(line[3], base=16)
        direction = None
        # shortcut: Checking the if it's a highnumber connection to a reserved port or vise versa should cover like 90% of directionality cases. Check the linux ephermal port range (includea IANA suggestion) first (most tcp stacks should be using this)
        # then check the RFC6056 > 1024
        if remote_port >= 32768 and local_port < 32768:
            direction = "inbound"
        elif local_port >= 32768 and remote_port < 32768:
            direction = "outbound"
        elif remote_port >= 1024 and local_port < 1024:
            direction = "inbound"
        elif local_port >= 1024 and remote_port < 1024:
            direction = "outbound"
        elif local_port < 1024:
            direction = "inbound"

        # ignore listening sockets
        if state != 10:
            conn_list.add(
                Connection(
                    remote_address,
                    remote_port,
                    local_address,
                    local_port,
                    time.time(),
                    direction,
                )
            )
    return conn_list


def little_to_big_endian(hex_str):
    lit_hex = ""
    for num in range(len(hex_str) - 2, -2, -2):
        lit_hex += hex_str[num] + hex_str[num + 1]
    return lit_hex


# is this efficent? Hell no, but it'll work for now. I'd have to look into redoing the initial datastrucure if I wanted to avoid all this extra looping I think.
def generate_block_list(conn_list, recent_blocks, logger):
    block_cnt = {}
    block_list = []
    for conn in conn_list:
        if conn.direction == "inbound":
            if conn.remote_address in block_cnt.keys():
                # this if it is the same port duplicates will not be allowed in the set
                block_cnt[conn.remote_address]["ports"].add(conn.local_port)
                block_cnt[conn.remote_address]["local_addr"] = conn.local_address
            else:
                block_cnt[conn.remote_address] = {
                    "ports": set([conn.local_port]),
                    "local_address": conn.local_address,
                }
    logger.debug(f"DEBUG: {block_cnt}")
    block_addrs = [x[0] for x in recent_blocks]
    for item, value in block_cnt.items():
        if len(value["ports"]) > 3 and item not in block_addrs:
            block_list.append(item)
            ports = ",".join([str(x) for x in value["ports"]])
            logger.info(
                f"Port scan detected: {item} -> {value['local_address']} on ports {ports}"
            )
    logger.debug(f"{block_list}")
    return block_list


def parse_address(address):
    address, port = address.split(":")
    address = str(ipaddress.ip_address(int(little_to_big_endian(address), base=16)))
    # port numbers are big endian
    if port != "":
        port = int(port, base=16)
    else:
        port = 0
    return address, port


def block_addresses(conn_block_list, recent_blocks, logger):
    recent_block_ips = [x[0] for x in recent_blocks]
    for addr in conn_block_list:
        if addr not in recent_block_ips:
            logger.debug(f"DEBUG: blocking address {addr}")
            subprocess.run(["iptables", "-I", "INPUT", "-s", addr, "-j", "DROP"])
            recent_blocks.append((addr, time.time()))

    return recent_blocks


def prune_recent_blocks(recent_blocks, logger):
    new_recent_blocks = []
    # prune recent block list
    # we need to maintain this extra state so we do not block via iptables multiple times, this is also used to determine if a connection still returned from
    # /proc/net/tcp is just waiting to time as it has been blocked already and should not be readded
    cur_time = time.time()
    for key, value in recent_blocks:
        if cur_time - value < 60:
            new_recent_blocks.append((key, value))
        else:
            logger.debug(f"DEBUG: purge recent_blocks: {key}")
    return new_recent_blocks


def prune_connections(cur_connections, connections, logger):
    cur_time = time.time()
    for conn in connections.difference(cur_connections):
        if cur_time - conn.time > 60:
            # remove connections that no longer are active and are older than a minute
            connections.remove(conn)
        else:
            logger.debug(f"purging connection: {conn}")


def process_connections(cur_connections, connections, conn_counter, logger):
    for conn in cur_connections.difference(connections):
        conn_counter.inc()
        logger.debug(f"DEBUG: {conn}")
        connections.add(conn)
        if conn.direction == "inbound":
            logger.info(
                f"New Connection:  {conn.local_address}:{conn.local_port} <- {conn.remote_address}:{conn.remote_port}"
            )
        elif conn.direction == "outbound":
            logger.info(
                f"New Connection:  {conn.local_address}:{conn.local_port} -> {conn.remote_address}:{conn.remote_port}"
            )
        else:
            # unkown direction, this can happen if communication is like 8080 <-> 9000
            logger.info(
                f"New Connection:  {conn.local_address}:{conn.local_port} -- {conn.remote_address}:{conn.remote_port}"
            )
