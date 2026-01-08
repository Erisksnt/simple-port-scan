import argparse
import json
import csv
import datetime
import os

from scanner.port_scan import scan_port


VERBOSE_LEVEL = 0


def vlog(level: int, msg: str):
    if VERBOSE_LEVEL >= level:
        print(msg)


def export_to_csv(path: str, results: list[dict]):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["port", "service", "status", "banner"]
        )
        writer.writeheader()
        writer.writerows(results)


def export_to_json(path: str, results: list[dict]):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


def auto_name(ext: str) -> str:
    os.makedirs("scans", exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    return os.path.join("scans", f"scan-{ts}.{ext}")


def parse_ports(ports_str: str) -> list[int]:
    ports = []

    for item in ports_str.split(","):
        item = item.strip()

        if "-" in item:
            start, end = map(int, item.split("-"))
            ports.extend(range(start, end + 1))
        else:
            ports.append(int(item))

    return ports


# ---------- OUTPUT TABULAR ----------

def print_table(results: list[dict]):
    if not results:
        print("Nenhuma porta aberta encontrada.")
        return

    headers = ["Port", "Service", "Status"]
    rows = [
        [str(r["port"]), r["service"], r["status"]]
        for r in results
    ]

    col_widths = [
        max(len(row[i]) for row in rows + [headers])
        for i in range(len(headers))
    ]

    def line(left, mid, right, fill):
        return left + mid.join(fill * (w + 2) for w in col_widths) + right

    def row(values):
        return "│ " + " │ ".join(
            values[i].ljust(col_widths[i])
            for i in range(len(values))
        ) + " │"

    print(line("┌", "┬", "┐", "─"))
    print(row(headers))
    print(line("├", "┼", "┤", "─"))

    for r in rows:
        print(row(r))

    print(line("└", "┴", "┘", "─"))


def ask_export(results):
    print("\n💾 Deseja salvar o resultado?")
    print("1 — CSV")
    print("2 — JSON")
    print("3 — CSV + JSON")
    print("4 — Não salvar")

    choice = input("> ").strip()

    if choice == "1":
        path = auto_name("csv")
        export_to_csv(path, results)
        print(f"📁 CSV salvo automaticamente em: {path}")

    elif choice == "2":
        path = auto_name("json")
        export_to_json(path, results)
        print(f"📁 JSON salvo automaticamente em: {path}")

    elif choice == "3":
        path_csv = auto_name("csv")
        path_json = auto_name("json")
        export_to_csv(path_csv, results)
        export_to_json(path_json, results)
        print(f"📁 Arquivos salvos: {path_csv}, {path_json}")

    else:
        print("✔ Resultado não será salvo.")


def main():
    global VERBOSE_LEVEL

    parser = argparse.ArgumentParser(description="Simple Port Scanner")

    parser.add_argument("host", help="Host alvo do scan")

    parser.add_argument(
        "-p", "--ports",
        required=True,
        help="Lista de portas (ex: 80,443,8000 ou 20-25)"
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=0.5,
        help="Timeout por porta em segundos (default: 0.5)"
    )

    parser.add_argument("--csv", action="store_true", help="Salvar automaticamente em CSV")
    parser.add_argument("--json", action="store_true", help="Salvar automaticamente em JSON")

    parser.add_argument(
        "-v", "--verbose",
        action="count",
        default=0,
        help="Exibe detalhes do scan (-v, -vv, -vvv)"
    )

    args = parser.parse_args()
    VERBOSE_LEVEL = args.verbose

    ports = parse_ports(args.ports)
    host = args.host
    timeout = args.timeout

    vlog(1, f"[CONFIG] Timeout: {timeout}s")

    print(f"\n🔎 Scaneando {host}...\n")

    results = []

    for port in ports:
        vlog(1, f"[SCAN] Porta {port}/tcp")

        result = scan_port(host, port, timeout=timeout)

        if not result:
            vlog(2, f"[CLOSED] {port}/tcp")
            continue

        vlog(1, f"[OPEN] {port}/tcp -> {result['service']}")
        if result.get("banner"):
            vlog(3, f"[BANNER]\n{result['banner']}")

        results.append(result)

    # ----- OUTPUT -----
    if VERBOSE_LEVEL == 0:
        print_table(results)

    exported = False

    if args.csv:
        path = auto_name("csv")
        export_to_csv(path, results)
        print(f"\n📁 CSV salvo automaticamente em: {path}")
        exported = True

    if args.json:
        path = auto_name("json")
        export_to_json(path, results)
        print(f"\n📁 JSON salvo automaticamente em: {path}")
        exported = True

    if not exported:
        ask_export(results)

    print("\n✔ Scan concluído.")


if __name__ == "__main__":
    main()
