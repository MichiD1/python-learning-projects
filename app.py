import sqlite3
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("datenbank.db")
    cursor = conn.cursor()
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

    <form action="/add" method="POST">
        <h3>Neues Ticket anlegen</h3>
        <input type="text" name="titel" placeholder="Ticket-Titel (z.B. Bugfix Login-Seite)" required>
        <textarea name="beschreibung" placeholder="Beschreibung der Aufgabe..." rows="3"></textarea>
        <button type="submit">Ticket erstellen</button>
    </form>

    <div class="ticket-liste">
        <h3>Aktuelle Tickets im Backlog</h3>
        {% if aufgaben %}
            {% for aufgabe in aufgaben %}
                <div class="ticket">
                    <div>
                        <strong>{{ aufgabe[1] }}</strong><br>
                        <small style="color: #666;">{{ aufgabe[2] }}</small>
                    </div>
                    <div>
                        <span class="status-badge {% if aufgabe[3] == 'Offen' %}status-offen{% else %}status-erledigt{% endif %}">{{ aufgabe[3] }}</span>
                        {% if aufgabe[3] == 'Offen' %}
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

@app.route("/")
def index():
    conn = sqlite3.connect("datenbank.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, titel, beschreibung, status FROM aufgaben ORDER BY id DESC")
    alle_aufgaben = cursor.fetchall()
    conn.close()
    return render_template_string(HTML_TEMPLATE, aufgaben=alle_aufgaben)

@app.route("/add", methods=["POST"])
def add_aufgabe():
    titel = request.form.get("titel")
    beschreibung = request.form.get("beschreibung")
    conn = sqlite3.connect("datenbank.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO aufgaben (titel, beschreibung) VALUES (?, ?)", (titel, beschreibung))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/done/<int:aufgabe_id>")
def erledige_aufgabe(aufgabe_id):
    conn = sqlite3.connect("datenbank.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE aufgaben SET status = 'Erledigt' WHERE id = ?", (aufgabe_id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)