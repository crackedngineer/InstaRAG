import socket


def find_available_port(start_port=8112, max_attempts=100):
    """
    Find an available port starting from a given port number.

    :param start_port: Port number to start checking from (default: 8112)
    :param max_attempts: Maximum number of ports to check before giving up (default: 100)
    :return: The first available port or None if no available port is found.
    """

    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if (
                s.connect_ex(("0.0.0.0", port)) != 0
            ):  # If connection fails, port is free
                return port
    raise Exception("No available port found")
