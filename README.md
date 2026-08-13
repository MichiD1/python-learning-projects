### Python & IT Praxis-Projekte

Dieses Repository enthält meine Praxis- und Lernprojekte, die ich im Selbststudium zur Vorbereitung auf eine Ausbildung zum Fachinformatiker entwickelt habe. Die Projekte decken Kernbereiche der Anwendungsentwicklung (FIAE) und Systemintegration (FISI) ab. 

### Projekte

### FIAE Enterprise Ticket-System (app.py)

Ein webbasiertes Full-Stack-Ticketsystem zur Fehlerverfolgung (Bug-Tracking) und Aufgabenverwaltung, wie es in modernen IT-Unternehmen genutzt wird. 

* **Technologien**: Python, Flask, HTML/CSS, SQLite3 (SQL)
* **Funktionen**: Daten werden relational in einer SQL-Datenbank gespeichert, ausgelesen und über das Web-Frontend per Klick aktualisiert (CRUD-Prinzip).

### Enterprise Infrastructure & VM Manager (Hypervisor Simulation)

Ein praxisnahes Administrations-Werkzeug zur Simulation und Verwaltung virtueller Server-Infrastrukturen (ähnlich VMware vSphere / Proxmox). 

* **Technologien**: Python, SQLite3 (SQL)
* **Funktionen**: 

  * **Ressourcen-Management**: Automatische Überwachung von RAM-Kapazitäten. Ein Überlasten des Hauptservers wird durch ein mathematisches Limit aktiv blockiert.
  * **Server-Lebenszyklus**: Virtuelle Maschinen können live erstellt, gestartet, gestoppt und gelöscht werden.
* **Lerneffekt**: Verknüpfung von relationaler SQL-Logik mit zentralem Kapazitätsmanagement.

### Network & Infrastructure Monitor (network_monitor.py)

Ein automatisiertes Administrations-Werkzeug zur kontinuierlichen Überwachung kritischer Server-Infrastrukturen. 

* **Technologien**: Python, OS-Subprozesse (Ping-Diagnose)
* **Funktionen**: Prüft Server-Erreichbarkeiten via Ping-Befehl automatisiert im Netzwerk und gibt visuelle Farb-Alarme (grüne/rote Punkte) bei Systemausfällen aus.

### Enterprise IT-Security & Infrastructure Guide (IT_SECURITY_GUIDE.md)

Eine strukturierte Onboarding-Checkliste und Leitlinie für moderne Firmennetzwerke. 

* **Inhalt**: Dokumentation von Best Practices zur Einhaltung von Datensicherheit (DSGVO), logischer Netzwerktrennung (VLAN) und Disaster-Recovery-Protokollen bei Systemausfällen.

### Hardware-Lagerverwaltung (lager.py)

Ein interaktives Programm zur Verwaltung von Firmen-Hardware. 

* **Technologien**: Python, SQLite3 (SQL)
* **Funktionen**: Geräte im Lager registrieren, gesamte Lagerliste auslesen, Gegenstände gezielt über ihre ID löschen.

### Taschenrechner & Zahlenratespiel

Kleine Konsolen-Skripte zur Festigung der grundlegenden Programmierlogik (Schleifen, Bedingungen und Fehlerbehandlung). 

### Notes

Der Ordner "notes" enthält meine Lernnotizen zu den Programmen. 

*Die Entwicklung und Optimierung der Projekte erfolgt im zielgerichteten Selbststudium unter dem Einsatz von modernen KI-Tools (Prompt Engineering) zur Code-Analyse und Fehlerdiagnose.*