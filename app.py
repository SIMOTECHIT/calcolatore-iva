
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """<!doctype html>
<html>
<head>
  <title>Calcolatore Guadagno IVA</title>
  <style>
    body { font-family: Arial; padding: 2rem; }
    input, button { padding: 0.5rem; margin: 0.5rem 0; width: 100%; max-width: 300px; }
    .result { margin-top: 1rem; font-weight: bold; }
  </style>
</head>
<body>
  <h1>Calcolatore Guadagno (IVA Inclusa)</h1>
  <form method="post">
    <label>Prezzo di acquisto (IVA inclusa):</label><br>
    <input type="number" step="0.01" name="acquisto" required><br>
    <label>Prezzo di vendita (IVA inclusa):</label><br>
    <input type="number" step="0.01" name="vendita" required><br>
    <label>Aliquota IVA (%):</label><br>
    <input type="number" step="0.01" name="iva" value="22" required><br>
    <button type="submit">Calcola</button>
  </form>
  {% if risultato %}
    <div class="result">
      <p>Prezzo netto di acquisto: {{ risultato.acquisto_netto }} &euro;</p>
      <p>Prezzo netto di vendita: {{ risultato.vendita_netto }} &euro;</p>
      <p>Guadagno netto: <strong>{{ risultato.guadagno }} &euro;</strong></p>
    </div>
  {% endif %}
</body>
</html>"""

def calcola_guadagno(prezzo_acquisto_ivato, prezzo_vendita_ivato, aliquota_iva):
    coeff = 1 + (aliquota_iva / 100)
    acquisto_netto = prezzo_acquisto_ivato / coeff
    vendita_netto = prezzo_vendita_ivato / coeff
    guadagno = vendita_netto - acquisto_netto
    return {
        "acquisto_netto": round(acquisto_netto, 2),
        "vendita_netto": round(vendita_netto, 2),
        "guadagno": round(guadagno, 2)
    }

@app.route("/", methods=["GET", "POST"])
def index():
    risultato = None
    if request.method == "POST":
        acquisto = float(request.form["acquisto"])
        vendita = float(request.form["vendita"])
        iva = float(request.form["iva"])
        risultato = calcola_guadagno(acquisto, vendita, iva)
    return render_template_string(HTML_TEMPLATE, risultato=risultato)

if __name__ == "__main__":
    app.run(debug=True)
