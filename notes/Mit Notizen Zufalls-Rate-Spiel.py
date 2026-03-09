import random   # Zufallszahlen erzeugen

# Funktion für die Eingabe
def eingabe_zahl():
    while True:
        try:
            # input() fragt den Benutzer nach Text 
            # int() wandelt Text in eine Zahl um, damit man rechnen/vergleichen kann
            # return gibt die Zahl zurück, damit wir sie speichern können 
            return int(input("Rate eine Zahl zwischen 1 und 10: "))
        except ValueError:  # Wenn keine Zahl eingegeben wurde
            print("Bitte nur eine ganze Zahl eingeben!")
            
while True: # Äußere Schleife - eine neue Runde starten
    geheime_zahl = random.randint(1, 10) #Zufallszahl generieren
    versuche = 0    # Zähler starten
   
    


    while True: # Innere Schleife - der Spieler versucht zu raten
        eingabe = eingabe_zahl()    # Funktion aufrufen
        versuche += 1   # += erhöht die Variable um 1
    
        # Vergleiche
        if eingabe == geheime_zahl: # == bedeutet "gleich"
            print(f"Richtig! Du hast die Zahl in {versuche} Versuchen erraten.")
            # {} in f-String zeigt Variable an
            break   # Runde beenden, springt aus innerer Schleife 
        elif eingabe < geheime_zahl: # < bedeutet kleiner 
            print("Zu niedrig!")
        else:       # alles andere, also größer
            print("Zu hoch!")
        if versuche >= 4:    # maximal 4 Versuche 
            print(f"Leider verloren! Die Zahl war {geheime_zahl}. ")
            break


    # Frage ob Spieler nochmal spielen will
    # .lower() wandelt Großbuchstaben in kleine um
    # != bedeutet "nicht gleich"
    nochmal = input("Willst du nochmal spielen? (j/n): ").lower()
    if nochmal != "j": # alles außer "j" = spiel beenden
        print("Danke fürs Spielen! Auf Wiedersehen!")
        break
    


