from scanner.port_scan import scan_port
from scanner.banner_grabber import grab_banner

def scan_ports(
    host: str,
    ports: list[int],
    timeout: float = 0.5,
) -> list[dict]:

    results = []

    for port in ports:
        result = scan_port(host, port, timeout=timeout)

        if not result:
            continue

        results.append(result)

    return results
