# ==============================================================================
# LERN-NOTIZEN: NETZWERK-MONITOR (Lern-Version)
# ==============================================================================

# NOTIZ: os wird benötigt, um Befehle direkt an das Betriebssystem zu senden (z.B. os.system)
import os
# NOTIZ: platform hilft zu erkennen, ob das Skript gerade auf Windows, Mac oder Linux läuft
import platform
# NOTIZ: time wird hier genutzt, um das aktuelle Datum und die Uhrzeit zu formatieren
import time

# Die Server-Liste der Firma (Hier simulieren wir wichtige Systeme)
COMPANY_SERVER = {
    "Zentraler Datenbank-Server": "127.0.0.1",       # Dein eigener PC (Localhost)
    "Externes Cloud-Gateway": "8.8.8.8",            # Google DNS (zum Testen als Online-Server)
    "Firmen-WLAN Router": "192.168.1.1"              # Typische Router-IP
}

def ping_server(ip):
    # NOTIZ: Windows nutzt "ping -n 1", Linux/Mac nutzen "ping -c 1". 
    # Ein Ternary Operator (Kurz-If) entscheidet hier automatisch basierend auf platform.system().
    param = "-n" if platform.system().lower() == "windows" else "-c"
    
    # NOTIZ: "> /dev/null" (Linux) oder "> {os.devnull}" (Windows) leitet den Text-Output des Pings um.
    # Dadurch bleibt die Python-Konsole sauber und zeigt nicht den Standard-Ping-Text an.
    befehl = f"ping {param} 1 {ip} > {os.devnull} 2>&1" if platform.system().lower() == "windows" else f"ping {param} 1 {ip} > /dev/null 2>&1"
    
    # NOTIZ: os.system führt den Befehl in der CMD/Terminal aus. Wenn der Rückgabewert 0 ist, war der Ping erfolgreich (True).
    return os.system(befehl) == 0

def system_check():
    print("==================================================")
    print("ENTERPRISE - IT-INFRASTRUKTUR MONITOR v1.0")
    print("==================================================")
    # NOTIZ: strftime formatiert die Zeit. %Y=Jahr, %m=Monat, %d=Tag, %H=Stunde, %M=Minute, %S=Sekunde
    print(f"Zeitpunkt der Ueberpruefung: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # NOTIZ: Ein "Flag" (Boolean), das standardmäßig auf False steht. Es schaltet auf True, sobald nur ein Server offline ist.
    sicherheits_alarm = False

    # NOTIZ: .items() erlaubt es, in der for-Schleife gleichzeitig den Namen (Key) und die IP (Value) auszugeben
    for name, ip in COMPANY_SERVER.items():
        print(f"Pruefe System: {name} [{ip}]...")
        is_online = ping_server(ip)
        
        if is_online:
            print("🟢 STATUS: ONLINE - Verbindung stabil.")
        else:
            print("🔴 ALARM: OFFLINE! Systemausfall pruefen!")
            sicherheits_alarm = True # Flag wird aktiviert
        print("-" * 50)
        
    # NOTIZ: Abschluss-Auswertung basierend auf dem Status des Flags
    if sicherheits_alarm:
        print("\nWARNUNG: Ein System meldet kritische Fehler!")
    else:
        print("\nALLE SYSTEME SICHER: Keine Netzwerkfehler erkannt.")

# NOTIZ: Die Einstiegsschnittstelle. Verhindert, dass der Test automatisch startet, wenn diese Datei in ein anderes Skript importiert wird.
if __name__ == "__main__":
    system_check()
