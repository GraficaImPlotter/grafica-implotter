import requests

ACCESS_TOKEN = "APP_USR-2800773803181431-103111-ab1f57af96cd1e845c2bc87a02a85245-1215107629"

async def gerar_pix(valor):
    url = "https://api.mercadopago.com/v1/payments"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    body = {
        "transaction_amount": round(valor, 2),
        "description": "Pagamento Gráfica Implotter",
        "payment_method_id": "pix",
        "payer": {"email": "graficaimplotter@gmail.com"}
    }
    r = requests.post(url, headers=headers, json=body)
    data = r.json()
    imagem_url = data['point_of_interaction']['transaction_data']['qr_code_base64']

    import base64
    with open("comprovantes/qr_temp.png", "wb") as f:
        f.write(base64.b64decode(imagem_url))
    return "comprovantes/qr_temp.png"
