import os
import platform
import time

# Die Server-Liste der Firma (Hier simulieren wir wichtige Systeme)
COMPANY_SERVER = {
    "Zentraler Datenbank-Server": "127.0.0.1",       # Lokaler PC (Localhost)
    "Externes Cloud-Gateway": "8.8.8.8",            # Google DNS (zum Testen als Online-Server)
    "Firmen-WLAN Router": "192.168.1.1"              # Typische Router-IP
}

# Prüft die Erreichbarkeit einer IP-Adresse.
# Passt den Ping-Befehl automatisch an das Betriebssystem (Windows/Linux) an.
def ping_server(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    befehl = f"ping {param} 1 {ip} > {os.devnull} 2>&1" if platform.system().lower() == "windows" else f"ping {param} 1 {ip} > /dev/null 2>&1"
    return os.system(befehl) == 0

def system_check():
    print("==================================================")
    print("ENTERPRISE - IT-INFRASTRUKTUR MONITOR v1.0")
    print("==================================================")
    print(f"Zeitpunkt der Ueberpruefung: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    sicherheits_alarm = False

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

if __name__ == "__main__":
    system_check()
