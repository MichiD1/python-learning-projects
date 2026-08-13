# ==============================================================================
# LERN-NOTIZEN: WEB-BASIERTES FULL-STACK TICKET-SYSTEM (Lern-Version)
# ==============================================================================

# NOTIZ: sqlite3 steuert die relationale Datenbank für unsere Tickets.
import sqlite3

# NOTIZ: Flask ist das Web-Framework.
# - render_template_string: Erlaubt uns, HTML direkt aus einer Variablen im Code zu laden.
# - request: Verarbeitet Daten, die der Benutzer über die Webseite absendet (z.B. Formulare).
# - redirect: Leitet den Browser nach einer Aktion automatisch auf eine andere Seite um.
from flask import Flask, render_template_string, request, redirect

# NOTIZ: Hier wird die Flask-App initialisiert. __name__ hilft Flask, den Pfad des Projekts zu finden.
app = Flask(__name__)

def init_db():
    """Erstellt die virtuelle Infrastruktur-Datenbank, falls sie noch nicht existiert."""
    conn = sqlite3.connect("datenbank.db")
    cursor = conn.cursor()
    # NOTIZ: DEFAULT 'Offen' sorgt dafür, dass jedes neue Ticket automatisch den Status 'Offen' hat,
    # ohne dass wir diesen beim Eintragen manuell angeben müssen.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS aufgaben (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titel TEXT NOT NULL,
            beschreibung TEXT,
            status TEXT DEFAULT 'Offen'
        )
    """)
    conn.commit()
    conn.close()

# ==============================================================================
# NOTIZEN ZUM HTML-TEMPLATE (FRONTEND)
# ==============================================================================
# In diesem String steckt das komplette Design und die Struktur der Webseite.
# Besonderheit hier sind die geschweiften Klammern {% ... %}. Das ist Jinja2 (die Template-Engine von Flask).
# Sie erlaubt es uns, Python-Logik (wie Schleifen und Bedingungen) direkt in HTML zu schreiben!
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>FIAE Projekt - Ticketverwaltung</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; background-color: #f4f6f9; }
        h1 { color: #333; }
        form { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }
        input, textarea, select { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
        button { background-color: #007bff; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background-color: #0056b3; }
        .ticket-liste { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .ticket { padding: 15px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; }
        .ticket:last-child { border-bottom: none; }
        .status-badge { padding: 5px 10px; border-radius: 12px; font-size: 12px; font-weight: bold; }
        .status-offen { background-color: #ffc107; color: #212529; }
        .status-erledigt { background-color: #28a745; color: white; }
    </style>
</head>
<body>
    <h1>🎫 FIAE Enterprise Ticket-System</h1>
    <p>Projekt-Status: Datenbank-Anbindung aktiv (SQLite3)</p>

    <!-- NOTIZ: method="POST" schickt die eingegebenen Daten unsichtbar im Hintergrund an den Server -->
    <form action="/add" method="POST">
        <h3>Neues Ticket anlegen</h3>
        <input type="text" name="titel" placeholder="Ticket-Titel (z.B. Bugfix Login-Seite)" required>
        <textarea name="beschreibung" placeholder="Beschreibung der Aufgabe..." rows="3"></textarea>
        <button type="submit">Ticket erstellen</button>
    </form>

    <div class="ticket-liste">
        <h3>Aktuelle Tickets im Backlog</h3>
        
        <!-- NOTIZ: Jinja2-Bedingung. Wenn die Liste 'aufgaben' nicht leer ist, wird der Code ausgeführt -->
        {% if aufgaben %}
            <!-- NOTIZ: Jinja2-Schleife. Geht jedes Ticket einzeln durch, ähnlich wie ein 'for x in y' in Python -->
            {% for aufgabe in aufgaben %}
                <div class="ticket">
                    <div>
                        <!-- NOTIZ: Da wir SELECT id, titel, beschreibung... machen, ist aufgabe[1] der Titel und aufgabe[2] die Beschreibung -->
                        <strong>{{ aufgabe[1] }}</strong><br>
                        <small style="color: #666;">{{ aufgabe[2] }}</small>
                    </div>
                    <div>
                        <!-- NOTIZ: Ein Kurz-If in Jinja2 entscheidet, welche CSS-Farbe das Ticket bekommt (offen=gelb, erledigt=grün) -->
                        <span class="status-badge {% if aufgabe[3] == 'Offen' %}status-offen{% else %}status-erledigt{% endif %}">{{ aufgabe[3] }}</span>
                        
                        <!-- NOTIZ: Nur wenn das Ticket offen ist, zeigen wir den Button zum Schließen an -->
                        {% if aufgabe[3] == 'Offen' %}
                            <!-- NOTIZ: Dynamischer Link. Übergibt die ID des Tickets direkt an die URL (z.B. /done/5) -->
                            <a href="/done/{{ aufgabe[0] }}" style="margin-left: 10px; color: #007bff; text-decoration: none; font-size: 14px;">[Schließen]</a>
                        {% endif %}
                    </div>
                </div>
            {% endfor %}
        {% else %}
            <p>Keine Tickets vorhanden. Gut gearbeitet!</p>
        {% endif %}
    </div>
</body>
</html>
"""

# ==============================================================================
# FLASK BACKEND ROUTEN (Lern-Version)
# ==============================================================================

# NOTIZ: @app.route("/") definiert die Startseite. Wenn man die Adresse im Browser aufruft, 
# startet Flask automatisch die Funktion index() direkt darunter.
@app.route("/")
def index():
    conn = sqlite3.connect("datenbank.db")
    cursor = conn.cursor()
    # NOTIZ: ORDER BY id DESC sorgt dafür, dass die neuesten Tickets immer ganz oben auf der Webseite stehen.
    cursor.execute("SELECT id, titel, beschreibung, status FROM aufgaben ORDER BY id DESC")
    alle_aufgaben = cursor.fetchall()
    conn.close()
    # NOTIZ: Hier verknüpfen wir Backend und Frontend. Wir übergeben die SQL-Daten ('alle_aufgaben') 
    # unter dem Variablennamen 'aufgaben' an unser HTML-Template.
    return render_template_string(HTML_TEMPLATE, aufgaben=alle_aufgaben)

# NOTIZ: Diese Route reagiert nur auf POST-Anfragen (wenn das Formular abgeschickt wurde).
@app.route("/add", methods=["POST"])
def add_aufgabe():
    # NOTIZ: request.form.get liest die Daten aus den HTML-Eingabefeldern über deren 'name'-Attribut aus.
    titel = request.form.get("titel")
    beschreibung = request.form.get("beschreibung")
    
    conn = sqlite3.connect("datenbank.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO aufgaben (titel, beschreibung) VALUES (?, ?)", (titel, beschreibung))
    conn.commit()
    conn.close()
    
    # NOTIZ: Nach dem Speichern leiten wir den Nutzer sofort zurück auf die Startseite ("/") um.
    # Dadurch sieht er sein neu angelegtes Ticket sofort in der Liste.
    return redirect("/")

# NOTIZ: <int:aufgabe_id> ist eine dynamische URL-Variable. Flask liest die Zahl aus dem Link aus 
# und übergibt sie als Parameter direkt in unsere Funktion erledige_aufgabe().
@app.route("/done/<int:aufgabe_id>")
def erledige_aufgabe(aufgabe_id):
    conn = sqlite3.connect("datenbank.db")
    cursor = conn.cursor()
    # NOTIZ: Ändert den Status des gezielten Tickets auf 'Erledigt'
    cursor.execute("UPDATE aufgaben SET status = 'Erledigt' WHERE id = ?", (aufgabe_id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    init_db() # NOTIZ: Datenbank wird beim Starten der App als Erstes eingerichtet.
    # NOTIZ: debug=True startet den Entwicklungsmodus. Der Server startet bei Code-Änderungen 
    # automatisch neu und zeigt Fehlermeldungen direkt im Webbrowser an.
    app.run(debug=True)
