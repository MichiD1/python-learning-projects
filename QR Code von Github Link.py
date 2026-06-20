# Zuerst sicherstellen, dass qrcode installiert ist
# pip install qrcode[pil]

import qrcode

# Der Link, den du in einen QR-Code umwandeln willst
url = "https://github.com/MichiD1/python-learning-projects"

# QR-Code erzeugen
qr = qrcode.QRCode(
    version=1,  # Größe des QR-Codes (1 = klein, 40 = sehr groß)
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,  # Größe jedes "Kästchens" im QR-Code
    border=4,  # Breite des Randes
)

qr.add_data(url)
qr.make(fit=True)

# QR-Code als Bild speichern
img = qr.make_image(fill_color="black", back_color="white")
img.save("qrcode.png")

print("QR-Code wurde als 'qrcode.png' gespeichert!")
