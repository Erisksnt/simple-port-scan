import socket


def grab_banner(target: str, port: int, timeout: float = 2.0):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((target, port))

        data = sock.recv(1024)
        sock.close()

        banner = data.decode(errors="ignore").strip()
        return banner if banner else None

    except Exception:
        return None
