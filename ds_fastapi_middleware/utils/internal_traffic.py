"""Utils for ip handling"""

import struct
import socket


def is_private_ip(ip: str, networks: list = None):
    """
    Check if the IP belongs to private network blocks.
    @param ip: IP address to verify.
    @param networks: List of private network blocks.
    @return: True representing whether the IP belongs.
    """

    for network in networks:
        try:
            ipaddr = struct.unpack(">I", socket.inet_aton(ip))[0]
            netaddr, bits = network.split("/")

            network_low = struct.unpack(">I", socket.inet_aton(netaddr))[0]
            network_high = network_low | 1 << (32 - int(bits)) - 1

            if network_high >= ipaddr >= network_low:
                return True
        except Exception:  # nosec
            pass

    return False
