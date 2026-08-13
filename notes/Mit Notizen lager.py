# ==============================================================================
# LERN-NOTIZEN: HARDWARE-LAGERVERWALTUNG (Lern-Version)
# ==============================================================================

# NOTIZ: sqlite3 wird importiert, um eine lokale relationale SQL-Datenbank zu steuern.
import sqlite3

# NOTIZ: Hier wird die Verbindung global (außerhalb der Funktionen) geöffnet.
# Vorteil: Wir müssen nicht in jeder einzelnen Funktion "connect()" und "close()" tippen.
verbindung = sqlite3.connect("lager_inventar.db")
cursor = verbindung.cursor()

# NOTIZ: Erstellt die Tabelle 'hardware'. 
# TEXT steht für Zeichenketten. TEXT NOT NULL erzwingt, dass das Feld ausgefüllt sein muss.
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
    # NOTIZ: Die '?' sind Platzhalter (Prepared Statements). Sie verhindern, dass über die
    # Eingabefelder bösartiger SQL-Schadcode ausgeführt wird (Schutz vor SQL-Injection).
    cursor.execute("INSERT INTO hardware (geraet, seriennummer, zustand) VALUES (?, ?, ?)", (geraete_typ, sn_nummer, aktueller_zustand))
    
    verbindung.commit() # NOTIZ: commit() schreibt die neue Hardware-Zeile fest in die DB-Datei.
    print(f"Erfolg: {geraete_typ} wurde im Lager registriert.")


def alle_geraete_anzeigen():
    cursor.execute("SELECT * FROM hardware")
    
    # NOTIZ: fetchall() zieht alle gefundenen Datensätze als Liste von Datenpaketen (Tuples) in den Speicher.
    alle_eintraege = cursor.fetchall()
    
    print("\n--- AKTUELLES FIRMEN-LAGER ---")
    if not alle_eintraege: # NOTIZ: Prüft, ob die Liste leer ist
        print("Das Lager ist aktuell leer.")
    for geraet in alle_eintraege:
        # NOTIZ: Da 'geraet' ein Tuple ist, greifen wir mit eckigen Klammern auf die Spalten zu.
        # Index: [0] = ID, [1] = Gerätetyp, [2] = Seriennummer, [3] = Zustand.
        print(f"ID: {geraet[0]} | Typ: {geraet[1]} | S/N: {geraet[2]} | Status: {geraet[3]}")
    print("------------------------------\n")

def geraet_loeschen(geraet_id):
    # NOTIZ: .isdigit() ist eine String-Methode. Sie prüft vor dem SQL-Befehl, ob der Benutzer
    # wirklich nur Zahlen (0-9) eingegeben hat. Verhindert Fehler, falls jemand Buchstaben eintippt.
    if not geraet_id.isdigit():
        print("\n[Fehler] Bitte gib eine gültige numerische ID ein!")
        return # NOTIZ: Beendet die Funktion sofort, damit kein falscher Wert an SQL übergeben wird.
    
    cursor.execute("DELETE FROM hardware WHERE id = ?", (geraet_id,))
    verbindung.commit()
    print(f"\n[Erfolg] Gerät mit der ID {geraet_id} wurde aus dem Lager gelöscht!\n")


# ==============================================================================
# HAUPTPROGRAMM / INTERAKTIVES MENÜ (Lern-Version)
# ==============================================================================
while True:
    print("=== LAGER-VERWALTUNG ===")
    print("1: Alle Geräte anzeigen")
    print("2: Neues Gerät hinzufügen")
    print("3: Gerät ausbuchen (Löschen)") 
    print("4: Programm beenden")           
    
    # NOTIZ: .strip() entfernt versehentliche Leerzeichen vor oder nach der Eingabe (z.B. "1 " -> "1").
    auswahl = input("Bitte eine Zahl wählen (1-4): ").strip()
    
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
        alle_geraete_anzeigen() # NOTIZ: Zeigt dem Nutzer die IDs, damit er weiß, was er löschen kann.
        ziel_id = input("Welche ID soll gelöscht werden? ")
        geraet_loeschen(ziel_id)
        
    elif auswahl == "4":
        print("\nProgramm wird beendet. Auf Wiedersehen!")
        break # NOTIZ: Bricht die Endlosschleife ab, um zum Code nach der Schleife zu springen.
    else:
        print("\n[Fehler] Ungültige Auswahl! Bitte eine Zahl von 1 bis 4 eingeben.\n")
        
    print("="*28 + "\n") # NOTIZ: Multipliziert das Zeichen "=" 28-mal für eine saubere Trennlinie.

# NOTIZ: Ganz am Ende des Programms wird die Verbindung zur Datenbank-Datei sauber geschlossen.
verbindung.close()
