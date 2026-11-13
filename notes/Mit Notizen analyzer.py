# Benötigte Python-Werkzeuge (Module) laden
import csv  # Zum Erstellen von Excel-kompatiblen CSV-Tabellen
import re  # Zum Suchen und Ersetzen von Textmustern (wie IP-Adressen)
from datetime import datetime  # Für das aktuelle Datum und die Uhrzeit
from pathlib import Path  # Für den sicheren Umgang mit Dateipfaden


# Hauptfunktion definieren: Nimmt den Pfad zur Log-Datei und den Namen der Zieldatei entgegen
def analyze_log_file(log_path: str, output_csv: str) -> None:
    """Durchsucht eine Log-Datei nach Warnungen und Fehlern und exportiert sie als CSV."""
    path = Path(log_path)

    # Prüfen, ob die Log-Datei überhaupt existiert (verhindert einen Programmabsturz)
    if not path.exists():
        print(f"[Fehler] Die Datei '{log_path}' wurde nicht gefunden.")
        return  # Beendet die Funktion sofort, falls die Datei fehlt

    # Suchbegriffe festlegen und leere Speicher für Ergebnisse und Zähler anlegen
    alert_levels = ("WARNING", "ERROR", "CRITICAL")
    findings = []  # Liste für alle gefundenen Fehlerzeilen
    counts = {level: 0 for level in alert_levels}  # Zähler startet für jedes Wort bei 0
    total_lines = 0  # Zählt später alle gelesenen Zeilen mit

    # Log-Datei sicher öffnen (mit utf-8, damit Umlaute richtig gelesen werden)
    with path.open("r", encoding="utf-8") as file:
        # Datei Zeile für Zeile von oben nach unten durchgehen
        for line_number, line in enumerate(file, start=1):
            total_lines += 1  # Gesamtzeilenzähler um 1 erhöhen
            clean_line = line.strip()  # Unnötige Leerzeichen und Zeilenumbrüche am Rand entfernen

            # IP-Adressen aus Datenschutzgründen (DSGVO) automatisch unkenntlich machen
            clean_line = re.sub(r"\b\d{1,3}(?:\.\d{1,3}){3}\b", "[IP-ANONYMISIERT]", clean_line)

            # Prüfen, ob eines der Fehlerwörter in der aktuellen Zeile vorkommt
            for level in alert_levels:
                if f" {level} " in clean_line:
                    counts[level] += 1  # Treffer für dieses Fehlerwort hochzählen
                    # Gefundene Zeile mit Zeilennummer und Schweregrad in die Ergebnisliste packen
                    findings.append({
                        "Zeile": line_number,
                        "Schweregrad": level,
                        "Eintrag": clean_line
                    })
                    break  # Innere Schleife stoppen, da das Fehlerwort gefunden wurde

    # Neue CSV-Datei erstellen und alle gesammelten Fehler als Tabelle hineinschreiben
    with open(output_csv, mode="w", newline="", encoding="utf-8") as csv_file:
        fieldnames = ["Zeile", "Schweregrad", "Eintrag"]  # Spaltenüberschriften festlegen
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=";")  # Semikolon für deutsches Excel
        writer.writeheader()  # Überschriften in die erste Zeile schreiben
        writer.writerows(findings)  # Alle gefundenen Fehlerzeilen einfügen

    # Zusammenfassung im Terminal ausgeben
    print("=== IT-Logfile-Analyse abgeschlossen ===")
    print(f"Zeitpunkt: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    for level, total in counts.items():
        print(f"- {level}: {total} Treffer")

    # Kritische Fehler (ERROR + CRITICAL) zusammenrechnen
    critical_errors = counts["ERROR"] + counts["CRITICAL"]

    # Fehlerquote in Prozent berechnen (nur wenn mindestens 1 Zeile vorhanden ist)
    if total_lines > 0:
        error_rate = round((critical_errors / total_lines) * 100, 1)  # Auf 1 Nachkommastelle runden
    else:
        error_rate = 0.0

    # Statistik im Terminal anzeigen
    print(f"Geprüfte Zeilen gesamt: {total_lines}")
    print(f"Kritische Fehlerquote: {error_rate} %")
    print(f"\nReport gespeichert unter: {output_csv}")


# Startpunkt des Programms: Wird nur ausgeführt, wenn diese Datei direkt gestartet wird
if __name__ == "__main__":
    analyze_log_file("server.log", "fehler_report.csv")
