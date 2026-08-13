# ==============================================================================
# LERN-NOTIZEN: NETZWERK-MONITOR (Lern-Version)
# ==============================================================================

import os        # Für Betriebssystem-Befehle (os.system)
import platform  # Erkennt das Betriebssystem (Windows/Linux)
import time      # Für Datum und Uhrzeit

# Die Server-Liste der Firma (Hier simulieren wir wichtige Systeme)
COMPANY_SERVER = {
    "Zentraler Datenbank-Server": "127.0.0.1",       # Dein eigener PC (Localhost)
    "Externes Cloud-Gateway": "8.8.8.8",            # Google DNS (zum Testen als Online-Server)
    "Firmen-WLAN Router": "192.168.1.1"              # Typische Router-IP
}

def ping_server(ip):
    # NOTIZ: Unterscheidet "ping -n 1" (Windows) und "ping -c 1" (Linux/Mac) per Kurz-If (Ternary Operator)
    param = "-n" if platform.system().lower() == "windows" else "-c"
    
    # NOTIZ: Unterdrückt den Standard-Ping-Text in der Konsole, indem die Ausgabe ins "Nichts" umgeleitet wird
    befehl = f"ping {param} 1 {ip} > {os.devnull} 2>&1" if platform.system().lower() == "windows" else f"ping {param} 1 {ip} > /dev/null 2>&1"
    
    # NOTIZ: Führt den Befehl aus. Rückgabewert 0 bedeutet Erfolg (True)
    return os.system(befehl) == 0

def system_check():
    print("==================================================")
    print("ENTERPRISE - IT-INFRASTRUKTUR MONITOR v1.0")
    print("==================================================")
    # NOTIZ: Formatiert das Datum: %Y=Jahr, %m=Monat, %d=Tag, %H=Stunde, %M=Minute, %S=Sekunde
    print(f"Zeitpunkt der Ueberpruefung: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # NOTIZ: Status-Flag (Boolean). Schaltet auf True um, sobald ein Server offline ist
    sicherheits_alarm = False

    # NOTIZ: .items() liest gleichzeitig den Namen (Key) und die IP (Value) aus dem Dictionary
    for name, ip in COMPANY_SERVER.items():
        print(f"Pruefe System: {name} [{ip}]...")
        is_online = ping_server(ip)
        
        if is_online:
            print("🟢 STATUS: ONLINE - Verbindung stabil.")
        else:
            print("🔴 ALARM: OFFLINE! Systemausfall pruefen!")
            sicherheits_alarm = True 
        print("-" * 50)
        
    if sicherheits_alarm:
        print("\nWARNUNG: Ein System meldet kritische Fehler!")
    else:
        print("\nALLE SYSTEME SICHER: Keine Netzwerkfehler erkannt.")

# NOTIZ: Einstiegspunkt. Verhindert automatischen Start bei Modul-Importen in anderen Skripten
if __name__ == "__main__":
    system_check()

