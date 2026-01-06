import json
import csv
import argparse
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

from .port_scanner import scan_port
from .banner_grabber import grab_banner


# -----------------------------
# Converter GMT → BRT
# -----------------------------
def convert_gmt_to_brt(date_line: str):
    try:
        raw = date_line.replace("Date: ", "").strip()

        dt_utc = datetime.strptime(raw, "%a, %d %b %Y %H:%M:%S GMT")
        dt_utc = dt_utc.replace(tzinfo=ZoneInfo("UTC"))

        dt_brt = dt_utc.astimezone(ZoneInfo("America/Sao_Paulo"))

        return f"Date (BRT): {dt_brt.strftime('%Y-%m-%d %H:%M:%S')}"
    except Exception:
        return date_line


# -----------------------------
# Scan por range
# -----------------------------
def scan_range(host, start, end):
    results = []

    for port in range(start, end + 1):
        r = scan_port(host, port)
        if not r:
            continue

        banner = grab_banner(host, port)

        if banner:
            lines = banner.split("\n")
            for i, line in enumerate(lines):
                if line.startswith("Date:"):
                    lines[i] = convert_gmt_to_brt(line)
            banner = "\n".join(lines)

        r["banner"] = banner
        results.append(r)

    return results


# -----------------------------
# CLI
# -----------------------------
def main():
    parser = argparse.ArgumentParser(description="Port Scanner CLI")

    parser.add_argument("--host", required=True, help="Target host/IP")
    parser.add_argument("--ports", help="Comma-separated list of ports")
    parser.add_argument("--start-port", type=int, help="Start of port range")
    parser.add_argument("--end-port", type=int, help="End of port range")
    parser.add_argument("--json", help="Save results to JSON file")
    parser.add_argument("--csv", help="Save results to CSV file")

    args = parser.parse_args()

    results = []

    # ---- Lista de portas ----
    if args.ports:
        ports = [int(p) for p in args.ports.split(",")]

        for port in ports:
            r = scan_port(args.host, port)
            if not r:
                continue

            banner = grab_banner(args.host, port)

            if banner:
                lines = banner.split("\n")
                for i, line in enumerate(lines):
                    if line.startswith("Date:"):
                        lines[i] = convert_gmt_to_brt(line)
                banner = "\n".join(lines)

            r["banner"] = banner
            results.append(r)

    # ---- Range de portas ----
    elif args.start_port and args.end_port:
        results = scan_range(args.host, args.start_port, args.end_port)

    # ---- Nenhuma opção válida ----
    else:
        print("Use --ports ou --start-port + --end-port")
        return

    if not results:
        print("Nenhuma porta aberta encontrada.")
        return

    # ---- Output no terminal ----
    for r in results:
        print(f"[+] Porta {r['port']} aberta — {r['service']}")
        if r.get("banner"):
            first = r["banner"].split("\n")[0]
            print(f"    Banner: {first}")
        print("-" * 40)

    # ---- Salvar JSON ----
    if args.json:
        Path(args.json).write_text(
            json.dumps(results, indent=4, ensure_ascii=False),
            encoding="utf-8"
        )
        print(f"[+] Resultado salvo em {args.json}")

    # ---- Salvar CSV ----
    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        print(f"[+] Resultado salvo em {args.csv}")


if __name__ == "__main__":
    main()
