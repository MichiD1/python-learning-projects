import sqlite3
import random

def datenbank_einrichten():
    """Erstellt die virtuelle Infrastruktur-Datenbank, falls sie noch nicht existiert."""
    conn = sqlite3.connect("enterprise_infrastruktur.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS virtuelle_maschinen (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            betriebssystem TEXT NOT NULL,
            ram_gb INTEGER NOT NULL,
            cpu_kerne INTEGER NOT NULL,
            status TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def vm_erstellen(name, os_typ, ram, cpu):
    """Simuliert das Anlegen einer neuen VM mit Ressourcen-Prüfung."""
    # Definiere das maximale Limit des Hauptservers (Host)
    MAX_RAM = 32
    
    conn = sqlite3.connect("enterprise_infrastruktur.db")
    cursor = conn.cursor()
    
    # Berechne den aktuell genutzten RAM aller existierenden VMs
    cursor.execute("SELECT SUM(ram_gb) FROM virtuelle_maschinen")
    ergebnis = cursor.fetchone()[0]
    aktueller_ram = ergebnis if ergebnis is not None else 0
    
    # FISI-Prüfung: Ist noch genug Platz auf dem Host?
    if aktueller_ram + ram > MAX_RAM:
        print(f"\n[!] FEHLER: Nicht genügend Ressourcen! Verfügbar: {MAX_RAM - aktueller_ram}GB RAM. Benötigt: {ram}GB RAM.")
        conn.close()
        return

    cursor.execute(
        "INSERT INTO virtuelle_maschinen (name, betriebssystem, ram_gb, cpu_kerne, status) VALUES (?, ?, ?, ?, 'Offline')",
        (name, os_typ, ram, cpu)
    )
    conn.commit()
    conn.close()
    print(f"\n[+] SYSTEM-INFO: Virtueller Server '{name}' wurde erfolgreich bereitgestellt!")

def infrastruktur_anzeigen():
    """Listet alle simulierten Server-Ressourcen auf."""
    conn = sqlite3.connect("enterprise_infrastruktur.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM virtuelle_maschinen")
    vms = cursor.fetchall()
    conn.close()
    
    print("\n==================================================")
    print("      AKTUELLER STATUS DER UNTERNEHMENS-IT        ")
    print("==================================================")
    if not vms:
        print("Keine virtuellen Server im System registriert.")
    for vm in vms:
        # Simuliert Live-Auslastung im Betrieb (wichtiges FISI-Feature)
        auslastung = f" | CPU-Last: {random.randint(4, 38)}%" if vm[5] == "Online" else ""
        print(f"ID: {vm[0]} | Name: {vm[1]} [{vm[2]}] | RAM: {vm[3]}GB | Cores: {vm[4]} | Status: {vm[5]}{auslastung}")
    print("==================================================")

def vm_status_aendern(vm_id, neuer_status):
    """Simuliert das Starten oder Herunterfahren eines Servers."""
    conn = sqlite3.connect("enterprise_infrastruktur.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE virtuelle_maschinen SET status = ? WHERE id = ?", (neuer_status, vm_id))
    conn.commit()
    conn.close()
    print(f"\n[*] HYPERVISOR: Server-ID {vm_id} wechselt in den Zustand: {neuer_status}.")

def vm_loeschen(vm_id):
    """Löscht eine virtuelle Maschine endgültig aus der Datenbank."""
    conn = sqlite3.connect("enterprise_infrastruktur.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM virtuelle_maschinen WHERE id = ?", (vm_id,))
    conn.commit()
    conn.close()
    print(f"\n[X] WARNUNG: Server mit ID {vm_id} wurde dauerhaft deprovisioniert (gelöscht).")

# Hauptprogramm / Konsolen-Menü
datenbank_einrichten()

while True:
    print("\n==================================================")
    print("      ENTERPRISE INFRASTRUCTURE MANAGER          ")
    print("==================================================")
    print(" 1) Alle aktiven Server auflisten")
    print(" 2) Neuen virtuellen Server (VM) bereitstellen")
    print(" 3) Virtuellen Server STARTEN (Online)")
    print(" 4) Virtuellen Server STOPPEN (Offline)")
    print(" 5) Virtuellen Server LÖSCHEN (Deprovisionieren)")
    print(" 6) System-Manager beenden")
    print("==================================================")
    
    auswahl = input("Aktion wählen (1-6): ")
    
    if auswahl == "1":
        infrastruktur_anzeigen()
    elif auswahl == "2":
        name = input("Server-Name (z.B. SQL_Datenbank oder Web_Server): ")
        os_typ = input("Betriebssystem (Ubuntu_Linux / Windows_Server): ")
        ram = int(input("Arbeitsspeicher (GB RAM): "))
        cpu = int(input("Prozessorkerne (vCPUs): "))
        vm_erstellen(name, os_typ, ram, cpu)
    elif auswahl == "3":
        vm_id = int(input("ID des zu startenden Servers: "))
        vm_status_aendern(vm_id, "Online")
    elif auswahl == "4":
        vm_id = int(input("ID des zu stoppenden Servers: "))
        vm_status_aendern(vm_id, "Offline")
    elif auswahl == "5":
        vm_id = int(input("ID des zu LÖSCHENDEN Servers eingeben: "))
        bestaetigung = input(f"Möchtest du Server ID {vm_id} wirklich unwiderruflich löschen? (ja/nein): ")
        if bestaetigung.lower() == "ja":
            vm_loeschen(vm_id)
        else:
            print("\n[-] Löschvorgang abgebrochen.")
    elif auswahl == "6":
        print("\n[V] System-Manager sicher heruntergefahren. Auf Wiedersehen!")
        break
    else:
        print("\n[!] FEHLER: Ungültige Menüauswahl.")