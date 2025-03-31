import os
import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Ruta para la página principal
@app.route('/')
def index():
    return render_template_string(open('form.html').read())

# Ruta para recibir el formulario y enviar el correo
@app.route('/send_email', methods=['POST'])
def send_email():
    name = request.form['name']
    email = request.form['email']

    # Enviar correo usando la API de Mailgun
    send_simple_message(name, email)

    return "Correo enviado correctamente"

def send_simple_message(name, email):
    # Reemplazar 'API_KEY' con tu clave real de Mailgun
    api_key = os.getenv('API_KEY', 'tu_api_key')
    domain = 'sandbox4d2c52cdc8d14e8d926da2f43fac381f.mailgun.org'
    url = f"https://api.mailgun.net/v3/{domain}/messages"

    data = {
        "from": "Mailgun Sandbox <postmaster@sandbox4d2c52cdc8d14e8d926da2f43fac381f.mailgun.org>",
        "to": f"{name} <{email}>",
        "subject": f"Hello {name}",
        "template": "change_password",  # Asegúrate de tener la plantilla adecuada en Mailgun
        "h:X-Mailgun-Variables": f'{{"name": "{name}", "email": "{email}"}}'
    }

    response = requests.post(
        url,
        auth=("api", api_key),
        data=data
    )

    print(response.text)  # Puedes imprimir la respuesta para depuración

if __name__ == '__main__':
    app.run(debug=True)
