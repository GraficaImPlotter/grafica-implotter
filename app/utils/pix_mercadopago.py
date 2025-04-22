import httpx

ACCESS_TOKEN = "APP_USR-2800773803181431-103111-ab1f57af96cd1e845c2bc87a02a85245-1215107629"

async def gerar_pix(valor: float, descricao: str):
    url = "https://api.mercadopago.com/instore/orders/qr/seller/pos_1234"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    body = {
        "external_reference": "pedido123",
        "title": descricao,
        "notification_url": "https://webhook.site/teste",
        "total_amount": valor,
        "description": descricao
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=body)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro ao gerar PIX: {response.text}")
