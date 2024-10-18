
import re
import requests

# API keys y datos de conexión (cambiar por tus propios datos)
API_KEY_STRIPE = "pk_test_51QBAOiRrg3tvTxSsaHomRIFe7goEoZeCk8quqD9XX4RS5ajtJDLg8wYxUHjz0P2fenjv1rr2qlTjM1QENX7sUalQ008JXIpJhV"
API_SECRET_STRIPE = "sk_test_51QBAOiRrg3tvTxSsBshRZg0zsYo9j2v5HgAyHS22wQpgiKHXf5DtcrWDrWtC5U0hUOhdRfEnBdeKu91MdfltIXTD00SlQUR6kd"
API_URL_STRIPE = "https://api.stripe.com/v1"

def verificar_tarjeta(numero_tarjeta, fecha_caducidad, cvv):
    # Verificar formato de número de tarjeta
    if not re.match(r"^[0-9]{16}$", numero_tarjeta):
        return False, "Número de tarjeta inválido"

    # Verificar formato de fecha de caducidad
    if not re.match(r"^(0[1-9]|1[0-2])/\d{2}$", fecha_caducidad):
        return False, "Fecha de caducidad inválida"

    # Verificar formato de CVV
    if not re.match(r"^[0-9]{3,4}$", cvv):
        return False, "CVV inválido"

    # Llamar a la API de Stripe para verificar la tarjeta
    headers = {
        "Authorization": f"Bearer {API_KEY_STRIPE}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    datos = {
        "card[number]": numero_tarjeta,
        "card[exp_month]": fecha_caducidad.split("/")[0],
        "card[exp_year]": fecha_caducidad.split("/")[1],
        "card[cvc]": cvv
    }
    respuesta = requests.post(f"{API_URL_STRIPE}/tokens", headers=headers, data=datos)

    # Verificar si la tarjeta es válida
    if respuesta.status_code == 200:
        return True, "Tarjeta válida"
    else:
        return False, respuesta.json()["error"]["message"]

def main():
    numero_tarjeta = input("Ingrese el número de tarjeta: ")
    fecha_caducidad = input("Ingrese la fecha de caducidad (MM/AA): ")
    cvv = input("Ingrese el CVV: ")

    valido, mensaje = verificar_tarjeta(numero_tarjeta, fecha_caducidad, cvv)
    print(mensaje)

if __name__ == "__main__":
    main()