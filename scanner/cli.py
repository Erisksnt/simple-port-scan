import argparse
import datetime
import os

from scanner.core.scanner import scan_ports
from scanner.report import export_to_csv, export_to_json


VERBOSE_LEVEL = 0


def vlog(level: int, msg: str):
    if VERBOSE_LEVEL >= level:
        print(msg)


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
        print(f"📁 CSV salvo em: {path}")

    elif choice == "2":
        path = auto_name("json")
        export_to_json(path, results)
        print(f"📁 JSON salvo em: {path}")

    elif choice == "3":
        path_csv = auto_name("csv")
        path_json = auto_name("json")
        export_to_csv(path_csv, results)
        export_to_json(path_json, results)
        print(f"📁 Arquivos salvos:\n- {path_csv}\n- {path_json}")

    else:
        print("✔ Resultado não será salvo.")


def main():
    global VERBOSE_LEVEL

    parser = argparse.ArgumentParser(description="Python Port Scanner CLI")

    parser.add_argument("host", help="Host alvo do scan")

    parser.add_argument(
        "-p", "--ports",
        required=True,
        help="Lista de portas (ex: 80,443,8000 ou 1-1000)"
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=1.0,
        help="Timeout por porta (segundos)"
    )

    parser.add_argument(
        "--threads",
        type=int,
        default=50,
        help="Quantidade de threads (default: 50)"
    )

    parser.add_argument("--csv", action="store_true", help="Salvar automaticamente em CSV")
    parser.add_argument("--json", action="store_true", help="Salvar automaticamente em JSON")

    parser.add_argument(
        "-v", "--verbose",
        action="count",
        default=0,
        help="Modo verbose (-v, -vv, -vvv)"
    )

    args = parser.parse_args()
    VERBOSE_LEVEL = args.verbose

    ports = parse_ports(args.ports)

    print(f"\n🔎 Scaneando {args.host}")
    print(f"📌 Portas: {len(ports)} | Threads: {args.threads} | Timeout: {args.timeout}s\n")

    results = scan_ports(
        host=args.host,
        ports=ports,
        timeout=args.timeout,
        threads=args.threads,
        
    )

    if VERBOSE_LEVEL == 0:
        for r in results:
            print(f"{r['port']},{r['service']},{r['status']}")

    exported = False

    if args.csv:
        path = auto_name("csv")
        export_to_csv(path, results)
        print(f"\n📁 CSV salvo em: {path}")
        exported = True

    if args.json:
        path = auto_name("json")
        export_to_json(path, results)
        print(f"\n📁 JSON salvo em: {path}")
        exported = True

    if not exported:
        ask_export(results)

    print("\n✔ Scan concluído.")


if __name__ == "__main__":
    main()
