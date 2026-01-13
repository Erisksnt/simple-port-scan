import csv
import json


def export_to_csv(path: str, results: list[dict]):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["port", "service", "status", "banner"]
        )
        writer.writeheader()
        for row in results:
            writer.writerow(row)


def export_to_json(path: str, results: list[dict]):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
