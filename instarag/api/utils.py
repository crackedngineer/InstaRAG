import socket
import requests


async def get_private_ip():
    """Get the correct 192.168.x.x private IP address."""
    try:
        # Create a temporary socket connection to get the correct private IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))  # Google Public DNS
            private_ip = s.getsockname()[0]
        return private_ip
    except Exception:
        return None
