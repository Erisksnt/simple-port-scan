import json
import csv
import argparse
from pathlib import Path
from .port_scanner import scan_port, COMMON_PORTS
from .banner_grabber import grab_banner
from datetime import datetime
from zoneinfo import ZoneInfo

def scan_range(host, start, end):
    results = []

    for port in range(start, end + 1):
        result = scan_port(host, port)

        if result:
            result["banner"] = grab_banner(host, port)
            results.append(result)

    return results

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

def main():
    parser = argparse.ArgumentParser(description="Port Scanner CLI")

    parser.add_argument("--host", required=True, help="Target host/IP")
    parser.add_argument("--start-port", type=int, help="Start of port range")
    parser.add_argument("--end-port", type=int, help="End of port range")
    parser.add_argument("--ports", help="Comma-separated list of ports")
    parser.add_argument("--json", help="Save results to JSON file")
    parser.add_argument("--csv", help="Save results to CSV file")

    args = parser.parse_args()

    # ------------ MODOS DE EXECUÇÃO ------------

    if args.ports:
        ports = [int(p) for p in args.ports.split(",")]
        results = []

        for port in ports:
            r = scan_port(args.host, port)
            if r:
                r["banner"] = grab_banner(args.host, port)
                results.append(r)

    elif args.start_port and args.end_port:
        results = scan_range(args.host, args.start_port, args.end_port)

    else:
        # fallback → escanear portas comuns
        results = []
        for port in COMMON_PORTS.keys():
            r = scan_port(args.host, port)
            if r:
                r["banner"] = grab_banner(args.host, port)
                results.append(r)

    # ------------ NENHUM RESULTADO ------------
    if not results:
        print("Nenhuma porta aberta encontrada.")
        return

    # ------------ IMPRESSÃO NO TERMINAL ------------
    for r in results:
        print(f"[+] Porta {r['port']} aberta — {r['service']}")
        if r.get("banner"):
            first_line = r["banner"].split("\n")[0]
            print(f"    Banner: {first_line}")
        print("-" * 40)

    # ------------ EXPORTAR JSON ------------
    if args.json:
        Path(args.json).write_text(
            json.dumps(results, indent=4, ensure_ascii=False),
            encoding="utf-8"
        )
        print(f"\n[+] Resultado salvo em {args.json}")

    # ------------ EXPORTAR CSV ------------
    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

        print(f"[+] Resultado salvo em {args.csv}")

def convert_gmt_to_brt(date_line: str):
    try:
        raw = date_line.replace("Date: ", "").strip()
        dt_utc = datetime.strptime(raw, "%a, %d %b %Y %H:%M:%S GMT")
        dt_utc = dt_utc.replace(tzinfo=ZoneInfo("UTC"))
        dt_brt = dt_utc.astimezone(ZoneInfo("America/Sao_Paulo"))
        return f"Date (BRT): {dt_brt.strftime('%Y-%m-%d %H:%M:%S')}"
    except Exception:
        return date_line

if __name__ == "__main__":
    main()
