# ==============================================================================
# LERN-NOTIZEN: ENTERPRISE INFRASTRUCTURE MANAGER (Lern-Version)
# ==============================================================================

# NOTIZ: sqlite3 ermöglicht eine lokale relationale Datenbank. Die Daten werden in einer 
# einfachen Datei auf der Festplatte gespeichert, ohne dass man einen großen Datenbank-Server installieren muss.
import sqlite3  

# NOTIZ: random nutzen wir hier für die Funktion "randint(min, max)". 
# Sie würfelt bei jedem Aufruf eine zufällige Zahl, um eine schwankende CPU-Last im Betrieb darzustellen.
import random   

def datenbank_einrichten():
    """Erstellt die virtuelle Infrastruktur-Datenbank, falls sie noch nicht existiert."""
    # NOTIZ: .connect öffnet die Verbindung. Gibt es die Datei noch nicht, wird sie automatisch neu erstellt.
    conn = sqlite3.connect("enterprise_infrastruktur.db")
    
    # NOTIZ: Der Cursor ist wie ein digitaler Zeiger oder Eingabestift. 
    # Erst durch den Cursor können wir SQL-Befehle an die geöffnete Datenbank senden.
    cursor = conn.cursor()
    
    # NOTIZ: CREATE TABLE legt die Struktur fest. 
    # AUTOINCREMENT sorgt dafür, dass jede neue VM automatisch die nächste freie Nummer (1, 2, 3...) erhält.
    # NOT NULL bedeutet, dass dieses Feld beim Erstellen niemals leer gelassen werden darf.
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
    # NOTIZ: .commit() ist extrem wichtig! Es speichert die Änderungen (die Tabellenerstellung) endgültig.
    # Ohne commit() wären die Änderungen nach dem Schließen der Verbindung wieder weg.
    conn.commit()
    conn.close()

def vm_erstellen(name, os_typ, ram, cpu):
    """Simuliert das Anlegen einer neuen VM mit Ressourcen-Prüfung."""
    # Definiere das maximale Limit des Hauptservers (Host)
    MAX_RAM = 32
    
    conn = sqlite3.connect("enterprise_infrastruktur.db")
    cursor = conn.cursor()
    
    # NOTIZ: Die SQL-Funktion SUM() rechnet automatisch alle Zahlen in der Spalte 'ram_gb' zusammen.
    cursor.execute("SELECT SUM(ram_gb) FROM virtuelle_maschinen")
    
    # NOTIZ: .fetchone() holt die allererste Zeile des Ergebnisses. 
    # Da SUM() nur einen einzigen Gesamtwert liefert, greifen wir mit [0] auf das erste Element des Ergebnisses zu.
    ergebnis = cursor.fetchone()[0]
    
    # NOTIZ: Ein "Ternary Operator" (Kurz-If): Wenn die Datenbank komplett leer ist, liefert SQL den Wert "None".
    # Da man mit "None" nicht rechnen kann, wandeln wir es hier blitzschnell in eine 0 um.
    aktueller_ram = ergebnis if ergebnis is not None else 0
    
    # FISI-Prüfung: Ist noch genug Platz auf dem Host?
    if aktueller_ram + ram > MAX_RAM:
        print(f"\n[!] FEHLER: Nicht genügend Ressourcen! Verfügbar: {MAX_RAM - aktueller_ram}GB RAM. Benötigt: {ram}GB RAM.")
        conn.close()
        return # NOTIZ: Das 'return' bricht die Funktion sofort ab, damit der Code für das Eintragen (INSERT) gar nicht erst ausgeführt wird.

    # NOTIZ: Die Fragezeichen '?' sind Platzhalter. Die echten Daten werden danach als Tuple (name, os_typ...) übergeben.
    # Das ist ein Sicherheitsstandard gegen "SQL-Injections", damit niemand Schadcode in die Eingabefelder einschleusen kann.
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
    
    # NOTIZ: .fetchall() holt ALLE Zeilen aus der Tabelle und speichert sie als Liste ab.
    # Jede Zeile in dieser Liste ist ein "Tuple" (ein unveränderliches Datenpaket), das die Spaltenwerte enthält.
    vms = cursor.fetchall()
    conn.close()
    
    print("\n==================================================")
    print("      AKTUELLER STATUS DER UNTERNEHMENS-IT        ")
    print("==================================================")
    if not vms:
        print("Keine virtuellen Server im System registriert.")
    for vm in vms:
        # NOTIZ: Da 'vm' ein Datentupel ist, greifen wir per Index auf die Spalten zu.
        # vm[5] holt den 'status' (Spalte 6 in der DB, da wir bei 0 anfangen zu zählen: 0=id, 1=name, ..., 5=status).
        auslastung = f" | CPU-Last: {random.randint(4, 38)}%" if vm[5] == "Online" else ""
        print(f"ID: {vm[0]} | Name: {vm[1]} [{vm[2]}] | RAM: {vm[3]}GB | Cores: {vm[4]} | Status: {vm[5]}{auslastung}")
    print("==================================================")

def vm_status_aendern(vm_id, neuer_status):
    """Simuliert das Starten oder Herunterfahren eines Servers."""
    conn = sqlite3.connect("enterprise_infrastruktur.db")
    cursor = conn.cursor()
    # NOTIZ: UPDATE ändert bestehende Werte. 
    # Das "WHERE id = ?" ist kritisch: Vergisst man das, würde SQL den Status ALLER Server in der Datenbank ändern!
    cursor.execute("UPDATE virtuelle_maschinen SET status = ? WHERE id = ?", (neuer_status, vm_id))
    conn.commit()
    conn.close()
    print(f"\n[*] HYPERVISOR: Server-ID {vm_id} wechselt in den Zustand: {neuer_status}.")

def vm_loeschen(vm_id):
    """Löscht eine virtuelle Maschine endgültig aus der Datenbank."""
    conn = sqlite3.connect("enterprise_infrastruktur.db")
    cursor = conn.cursor()
    # NOTIZ: Bei nur einem Parameter im SQL-Befehl verlangt Python bei den Platzhaltern trotzdem ein Tuple.
    # Das Komma bei "(vm_id,)" zwingt Python dazu, es als Tuple und nicht als einfache Klammerung zu lesen.
    cursor.execute("DELETE FROM virtuelle_maschinen WHERE id = ?", (vm_id,))
    conn.commit()
    conn.close()
    print(f"\n[X] WARNUNG: Server mit ID {vm_id} wurde dauerhaft deprovisioniert (gelöscht).")
