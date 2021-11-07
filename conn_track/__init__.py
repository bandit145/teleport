import conn_track.utils as utils
import time
import sys
import os
import logging
from prometheus_client import Counter, start_http_server


def read_file():
    with open("/proc/net/tcp", mode="r") as net_ncp:
        return net_ncp.read().strip().split("\n")


def run():
    log_level = os.getenv("LOGGING_LEVEL")
    if not log_level:
        log_level = "info"
    logging.basicConfig(
        stream=sys.stdout,
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s %(message)s",
        datefmt="%Y-%d-%d %H:%M:%S",
    )
    try:
        # gather initial connections. We don't less these because we consider them existing
        connections = utils.parse_net_tcp(read_file())
        conn_counter = Counter("new_connections", "Number of new connections")
        recent_blocks = []
        start_http_server(9000)
        while True:
            time.sleep(10)
            cur_time = time.time()
            cur_connections = utils.parse_net_tcp(read_file())
            utils.prune_connections(cur_connections, connections, cur_time, logging)
            utils.process_connections(
                cur_connections, connections, conn_counter, logging
            )
            recent_blocks = utils.block_addresses(
                utils.generate_block_list(
                    connections, recent_blocks, cur_time, logging
                ),
                recent_blocks,
                logging,
            )
            recent_blocks = utils.prune_recent_blocks(recent_blocks, cur_time, logging)
    except KeyboardInterrupt:
        print("User exited")
        sys.exit(0)
