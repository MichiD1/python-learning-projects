# Python & IT Praxis-Projekte

Dieses Repository enthält meine Praxis- und Lernprojekte, die ich im Selbststudium zur Vorbereitung auf eine Ausbildung zum Fachinformatiker entwickelt habe. Die Projekte decken Kernbereiche der Anwendungsentwicklung (FIAE) und Systemintegration (FISI) ab.

---

## 📁 Projekte & Struktur

### 1. FIAE Enterprise Ticket-System (`/ticket-system`)
Ein webbasiertes Full-Stack-Ticketsystem zur Fehlerverfolgung (Bug-Tracking) und Aufgabenverwaltung, wie es in modernen IT-Unternehmen genutzt wird.
- **Technologien**: Python, Flask, HTML/CSS, SQLite3 (SQL)
- **Funktionen**: Daten werden relational in einer SQL-Datenbank gespeichert, ausgelesen und über das Web-Frontend per Klick aktualisiert (CRUD-Prinzip).

### 2. Enterprise Infrastructure & VM Manager (`/hypervisor-simulation`)
Ein praxisnahes Administrations-Werkzeug zur Simulation und Verwaltung virtueller Server-Infrastrukturen (ähnlich VMware vSphere / Proxmox).
- **Technologien**: Python, SQLite3 (SQL)
- **Funktionen**:
  - **Ressourcen-Management**: Automatische Überwachung von RAM-Kapazitäten. Ein Überlasten des Hauptservers wird durch ein mathematisches Limit aktiv blockiert.
  - **Server-Lebenszyklus**: Virtuelle Maschinen können live erstellt, gestartet, gestoppt und gelöscht werden.
  - **Lerneffekt**: Verknüpfung von relationaler SQL-Logik mit zentralem Kapazitätsmanagement.

### 3. Network & Infrastructure Monitor (`/network-monitor`)
Ein automatisiertes Administrations-Werkzeug zur kontinuierlichen Überwachung kritischer Server-Infrastrukturen.
- **Technologien**: Python, OS-Subprozesse (Ping-Diagnose)
- **Funktionen**: Prüft Server-Erreichbarkeiten via Ping-Befehl automatisiert im Netzwerk und gibt visuelle Farb-Alarme (grüne/rote Punkte) bei Systemausfällen aus.

### 4. Hardware-Lagerverwaltung & Scripts (`/kleine-tools`)
Ein interaktives Programm zur Verwaltung von Firmen-Hardware sowie kleine Konsolen-Skripte zur Festigung der grundlegenden Programmierlogik (Schleifen, Bedingungen und Fehlerbehandlung).
- **Inhalt**: `lager.py` (Geräte registrieren, Lagerliste auslesen, IDs löschen), Taschenrechner & Zahlenratespiel.

### 5. Enterprise IT-Security & Infrastructure Guide (`IT_SECURITY_GUIDE.md`)
Eine strukturierte Onboarding-Checkliste und Leitlinie für moderne Firmennetzwerke.
- **Inhalt**: Dokumentation von Best Practices zur Einhaltung von Datensicherheit (DSGVO), logischer Netzwerktrennung (VLAN) und Disaster-Recovery-Protokollen bei Systemausfällen.

### 6. IT-Logfile-Analyzer & CSV-Report Generator ( /log-analyzer )

Ein automatisiertes Python-Werkzeug zur Auswertung von Server-Logdateien, Berechnung von Fehlerquoten und DSGVO-konformen Berichterstellung.

- **Technologien**: Python (`pathlib`, `csv`, `re` / Regular Expressions)
- **Funktionen**:
  - **Fehler-Erkennung & Statistik**: Durchsucht Server-Logs automatisiert nach `WARNING`, `ERROR` und `CRITICAL` und berechnet die kritische Fehlerquote in Prozent.
  - **DSGVO-Datenschutz**: Erkennt IPv4-Adressen per RegEx und ersetzt sie vor dem Export automatisch durch `[IP-ANONYMISIERT]`.
  - **CSV-Export**: Erstellt einen Excel-kompatiblen Fehlerbericht (`;`-getrennt, UTF-8) für die IT-Administration.

---

## 🛠️ Installation & Setup

1. **Repository klonen:**
   ```bash
   git clone https://github.com/MichiD1/python-learning-projects
   ```
2. **Abhängigkeiten installieren:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Hinweis zu den Datenbanken:** 
   Lokale SQLite-Datenbankdateien (`*.db`) werden über die `.gitignore` bewusst vom Repository ausgeschlossen, um saubere Quellcodes zu wahren. Sie werden beim ersten Programmstart lokal automatisch generiert.

---

## 📝 Notes
Der Ordner `notes` enthält meine Lernnotizen zu den Programmen.

*Die Entwicklung und Optimierung der Projekte erfolgt im zielgerichteten Selbststudium unter dem Einsatz von modernen KI-Tools (Prompt Engineering) zur Code-Analyse und Fehlerdiagnose.*
