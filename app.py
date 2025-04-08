from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
  <title>Calcolatore Guadagno IVA</title>
  <style>
    body { font-family: Arial, sans-serif; padding: 2rem; background-color: #f4f4f4; }
    h1 { color: #333; }
    form { background: #fff; padding: 2rem; border-radius: 8px; max-width: 400px; margin: auto; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
    input, button { padding: 0.5rem; margin: 0.5rem 0; width: 100%; box-sizing: border-box; }
    .result { margin-top: 1rem; font-weight: bold; color: #005b4f; }
  </style>
</head>
<body>
  <h1 style="text-align:center;">Calcolatore Guadagno (IVA Inclusa)</h1>
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
      <p>Prezzo netto di acquisto: {{ risultato.acquisto_netto }} €</p>
      <p>Prezzo netto di vendita: {{ risultato.vendita_netto }} €</p>
      <p>Guadagno netto: <strong>{{ risultato.guadagno }} €</strong></p>
    </div>
  {% endif %}
</body>
</html>
"""

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
