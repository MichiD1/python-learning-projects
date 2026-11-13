import csv
import re
from datetime import datetime
from pathlib import Path

def analyze_log_file(log_path: str, output_csv: str) -> None:
    """Durchsucht eine Log-Datei nach Warnungen und Fehlern und exportiert sie als CSV."""
    path = Path(log_path)

    if not path.exists():
        print(f"[Fehler] Die Datei ´ {log_path}´ wurde nicht gefunden.")
        return

    alert_levels = ("WARNING", "ERROR", "CRITICAL")
    findings = []
    counts = {level: 0 for level in alert_levels}
    total_lines = 0
    
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            total_lines += 1
            clean_line = line.strip()
            # IP-Adressen automatisch nach DSGVO-Standard anonymisieren
            clean_line = re.sub(r"\b\d{1,3}(?:\.\d{1,3}){3}\b", "[IP-ANONYMISIERT]", clean_line)

            for level in alert_levels:
                if f" {level} " in clean_line:
                    counts[level] += 1
                    findings.append({
                        "Zeile": line_number,
                        "Schweregrad": level,
                        "Eintrag": clean_line
                    })
                    break
    with open(output_csv, mode="w", newline="", encoding="utf-8") as csv_file:
        fieldnames = ["Zeile", "Schweregrad", "Eintrag"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(findings)

    print("=== IT-Logfile-Analyse abgeschlossen ===")
    print(f"Zeitpunkt: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    for level, total in counts.items():
        print(f"- {level}: {total} Treffer")

    critical_errors = counts["ERROR"] + counts["CRITICAL"]

    if total_lines > 0:
        error_rate = round((critical_errors / total_lines) * 100, 1)
    else:
        error_rate = 0.0
    print(f"Geprüfte Zeilen gesamt: {total_lines}")
    print(f"Kritische Fehlerquote: {error_rate} %")
    print(f"\nReport gespeichert unter: {output_csv}")

if __name__ == "__main__":
    analyze_log_file("server.log", "fehler_report.csv")
