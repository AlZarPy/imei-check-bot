import json
import aiohttp

from config import API_TOKEN
from services import get_service_id

async def check_imei(imei: str):   # Функция для проверки IMEI через API
    url = 'https://api.imeicheck.net/v1/checks'
    token = API_TOKEN
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    # Получение service_id из services.py
    service_id = get_service_id()

    payload = json.dumps({
        'deviceId': imei,
        'serviceId': service_id
    })

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as response:
                print(f"Response status: {response.status}")  # Выводим статус ответа
                print(f"Response body: {await response.text()}")  # Выводим тело ответа

                if response.status == 201:
                    response_json = await response.json()
                    return response_json.get("properties", {})  # Возвращаем только поле properties
                elif response.status == 401:
                    return {"error": "The authorization token is missing or invalid."}
                elif response.status == 402:
                    return {"error": "Your account balance is insufficient for this order."}
                elif response.status == 422:
                    return {"error": "Request data validation error."}
                elif response.status >= 500:
                    return {"error": "Please try again later or contact support."}
                else:
                    return {"error": f"Неизвестная ошибка. Код ответа: {response.status}"}
    except aiohttp.ClientError as e:
        return {'error': f'Ошибка сети: {str(e)}'}
    except Exception as e:
        return {'error': f'Неизвестная ошибка: {str(e)}'}
