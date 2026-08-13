###  Enterprise IT-Security & Infrastructure Guide

**Best Practices für IT-Sicherheit, Netzwerkinfrastruktur und Datenschutz (DSGVO)**


Dieses Dokument dient als universelle Richtlinie und Onboarding-Checkliste für moderne Unternehmens-Netzwerke, um sensible Firmendaten zu schützen und Systemausfälle zu verhindern. 

### 1. Arbeitsplatz-Sicherheit & Datenschutz

* [ ] **Sichere Bildschirmsperre (Win + L):** Konsequentes Sperren des Desktops beim Verlassen des Arbeitsplatzes, um unbefugten Zugriff auf sensible Daten (DSGVO) zu verhindern.
* [ ] **Wechselmedien-Richtlinie (USB-Sperre):** Striktes Verbot privater Datenträger an Firmen-Clients zur Vermeidung von Schadsoftware-Infektionen (Ransomware).
* [ ] **Clean Desk Policy:** Sichere Verwahrung von Zugangsdaten; Verbot physischer Passwort-Notizen am Arbeitsplatz.

### 2. Netzwerk-Architektur & Gerätesicherheit

* [ ] **Strikte Netztrennung (VLAN):** Physische und logische Trennung zwischen dem produktiven Firmennetzwerk, der Server-Infrastruktur und dem öffentlichen Gäste-WLAN.
* [ ] **Zentrales Patch-Management:** Automatisierte wöchentliche Überprüfung und Einspielung von Sicherheitsupdates auf allen Clients und Servern.
* [ ] **Peripherie-Überwachung:** Systematische Kontrolle von Netzwerk-Druckern und Hardware-Komponenten auf unbefugte Modifikationen.

### 3. IT-Notfall-Protokoll bei Systemausfall (Disaster Recovery)

1. **Isolierung:** Sofortige Trennung des betroffenen Netzwerksegments vom Hauptswitch, um eine Ausbreitung von Fehlern oder Schadsoftware to stoppen.
2. **Diagnose:** Analyse der Server-Logs und Systemauslastung zur schnellen Lokalisierung der Fehlerquelle.
3. **Wiederherstellung:** Einspielen des letzten konsistenten Backups (Daily Backup) und schrittweise Reaktivierung der Systemdienste.