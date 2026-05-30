import sqlite3


verbindung = sqlite3.connect("lager_inventar.db")


cursor = verbindung.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS hardware (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    geraet TEXT NOT NULL,
    seriennummer TEXT,
    zustand TEXT
)
""")
verbindung.commit()

print("Datenbank wurde erfolgreich vorbereitet!")

def geraet_hinzufuegen(geraete_typ, sn_nummer, aktueller_zustand):
    
    cursor.execute("INSERT INTO hardware (geraet, seriennummer, zustand) VALUES (?, ?, ?)", (geraete_typ, sn_nummer, aktueller_zustand))
    
    verbindung.commit()
    print(f"Erfolg: {geraete_typ} wurde im Lager registriert.")
geraet_hinzufuegen("Monitor 24 Zoll", "SN-554433", "neu")

def alle_geraete_anzeigen():
    cursor.execute("SELECT * FROM hardware")
    
    alle_eintraege = cursor.fetchall()
    
    print("\n--- AKTUELLES FIRMEN-LAGER ---")
    for geraet in alle_eintraege:
        print(f"ID: {geraet[0]} | Typ: {geraet[1]} | S/N: {geraet[2]} | Status: {geraet[3]}")
    print("------------------------------\n")
def geraet_loeschen(geraet_id):
    
    cursor.execute("DELETE FROM hardware WHERE id = ?", (geraet_id,))
    verbindung.commit()
    print(f"\n[Erfolg] Gerät mit der ID {geraet_id} wurde aus dem Lager gelöscht!\n")


while True:
    print("=== LAGER-VERWALTUNG ===")
    print("1: Alle Geräte anzeigen")
    print("2: Neues Gerät hinzufügen")
    print("3: Gerät ausbuchen (Löschen)") 
    print("4: Programm beenden")           
    
    auswahl = input("Bitte eine Zahl wählen (1-4): ")
    
    if auswahl == "1":
        alle_geraete_anzeigen()
        
    elif auswahl == "2":
        print("\n--- NEUES GERÄT EINTRAGEN ---")
        typ = input("Welches Gerät (z.B. Laptop)? ")
        sn = input("Seriennummer? ")
        zustand = input("Zustand (z.B. neu)? ")
        geraet_hinzufuegen(typ, sn, zustand)
        
    elif auswahl == "3":
        print("\n--- GERÄT LÖSCHEN ---")
        alle_geraete_anzeigen() 
        ziel_id = input("Welche ID soll gelöscht werden? ")
        geraet_loeschen(ziel_id)
        
    elif auswahl == "4":
        print("\nProgramm wird beendet. Auf Wiedersehen!")
        break
        
    print("="*28 + "\n")

    verbindung.close()
