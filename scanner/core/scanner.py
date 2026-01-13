from concurrent.futures import ThreadPoolExecutor, as_completed
from scanner.port_scan import scan_port


def scan_ports(
    host: str,
    ports: list[int],
    timeout: float = 0.5,
    threads: int = 50
) -> list[dict]:
    """
    Scan múltiplas portas usando threading.
    Retorna apenas portas abertas.
    """

    results = []

    def worker(port: int):
        return scan_port(host, port, timeout=timeout)

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(worker, port): port for port in ports}

        for future in as_completed(futures):
            try:
                result = future.result()
                if result:
                    results.append(result)
            except Exception:
                # evita que uma thread quebre o scan inteiro
                pass

    return sorted(results, key=lambda r: r["port"])
