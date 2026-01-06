from .banner_grabber import grab_banner
import socket

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "TELNET",
    25: "SMTP",
    80: "HTTP",
    443: "HTTPS",
    8000: "HTTP-ALT",  
    3306: "MySQL"
}
def scan_port(target: str, port: int, timeout: float = 0.5):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    try:
        result = sock.connect_ex((target, port))
        if result == 0:
            banner = grab_banner(target, port)
            return {
                "port": port,
                "service": COMMON_PORTS.get(port, "UNKNOWN"),
                "status": "open",
                "banner": banner
            }
    except socket.error:
        pass
    finally:
        sock.close()

    return None

def scan_range(host, start, end):
    results = []
    try:
        for port in range(start, end + 1):
            result = scan_port(host, port)
            if result:
                results.append(result)
        return results

    except KeyboardInterrupt:
        print("\n[!] Scan interrompido pelo usuário.")
        return results

def scan_target(target: str):
    results = []

    for port, service in COMMON_PORTS.items():

        if not scan_port(target, port):
            continue

        banner = grab_banner(target, port)

        results.append({
            "port": port,
            "service": service,
            "status": "open",
            "banner": banner
        })

    return results
