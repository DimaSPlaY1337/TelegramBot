import asyncio
import ctypes
import os
import aiohttp
import hashlib
import time
from datetime import datetime
from typing import Optional
import http.client
import json
import pyautogui
from PIL import Image

# "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJHR1NlbGxlciIsInN1YiI6NjU2OCwiaWF0IjoxNzYxMDY3NTM0LCJleHAiOjE3NjM3NDU5MzQsImp0aSI6IjVlODlhMzk4LTNiYzItNDYxOC1hNGQ5LTBjMTAxNDk5MDY5YiIsInVzZXIiOnsiaWQiOjY1NjgsImVtYWlsIjoibWFya3R2ZW5ib29zdEBnbWFpbC5jb20ifSwidXVpZCI6IjllMmY2MmRlLWVkOWYtNGZlYS1hMjBmLWVkODc2ZjgxNTJlYSJ9.GSkQr6UVr8YNn1t_o3A1r-7ue98rszhUGkKwKEqI_qA"

API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJHR1NlbGxlciIsInN1YiI6NjU2OCwiaWF0IjoxNzYxMDY3NTM0LCJleHAiOjE3NjM3NDU5MzQsImp0aSI6IjVlODlhMzk4LTNiYzItNDYxOC1hNGQ5LTBjMTAxNDk5MDY5YiIsInVzZXIiOnsiaWQiOjY1NjgsImVtYWlsIjoibWFya3R2ZW5ib29zdEBnbWFpbC5jb20ifSwidXVpZCI6IjllMmY2MmRlLWVkOWYtNGZlYS1hMjBmLWVkODc2ZjgxNTJlYSJ9.GSkQr6UVr8YNn1t_o3A1r-7ue98rszhUGkKwKEqI_qA"
SELLER_ID = 889983

# Множество для хранения ID обработанных продаж
processed_sales = set()
customers_count = 10
# Система очереди
order_queue = []  # Очередь заказов [(dialog_id, customer, timestamp)]
current_processing = None  # Текущий обрабатываемый заказ
queue_lock = asyncio.Lock()# Lock гарантирует, что в один момент времени только одна корутина сможет получить доступ к защищенному ресурсу или выполнить критическую секцию кода.

# async def get_token():
#     conn = None
#     try:
#         conn = http.client.HTTPSConnection("seller.ggsel.net")
#         payload = json.dumps({
#             "seller_id": 0,
#             "timestamp": "string",
#             "sign": "string"
#         })
#         headers = {
#             'Content-Type': 'application/json',
#             'Accept': 'application/json'
#         }
#         conn.request("POST", "/api_sellers/api/apilogin", payload, headers)
#         res = conn.getresponse()
#         if res.status == 200:
#             data = res.read()
#             return json.loads(data.decode("utf-8"))
#         else:
#             raise Exception(f"API Error: {res.status} - {res.reason}")
#     except Exception as e:
#         print(f"Error: {e}")
#         return None
#     finally:
#         conn.close()

async def get_token():

    url = "https://seller.ggsel.net/api_sellers/api/apilogin"
    timestamp = int(time.time())
    sign_source = f"{API_KEY}{timestamp}"
    sign = hashlib.sha256(sign_source.encode()).hexdigest()
    payload = {
        "seller_id": SELLER_ID,
        "timestamp": timestamp,
        "sign": sign
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            response.raise_for_status()
            data = await response.json()
            return data["token"]

# async def get_dialogs(token):
#     conn = None
#     try:
#         conn = http.client.HTTPSConnection("seller.ggsel.net")
#         headers = {
#             'Accept': 'application/json'
#         }
#
#         # Формируем URL с токеном
#         url = f"/api_sellers/api/debates/v2/chats?token={token}"
#
#         conn.request("GET", url, '', headers)
#         res = conn.getresponse()
#
#         # Проверяем статус ответа
#         if res.status == 200:
#             data = res.read()
#             return json.loads(data.decode("utf-8"))
#         else:
#             raise Exception(f"API Error: {res.status} - {res.reason}")
#
#     except Exception as e:
#         print(f"Error: {e}")
#         return None
#     finally:
#         conn.close()

async def get_dialogs(token):
    url = f"https://seller.ggsel.net/api_sellers/api/debates/v2/chats?token={token}"
    headers = {"Accept": "application/json"}
    # params = {
    #     "filter_new": 1
    # }
    # , params = params
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            return await response.json()

# async def get_messages(token, dialog_id):
#     conn = None
#     try:
#         conn = http.client.HTTPSConnection("seller.ggsel.net")
#         payload = ''
#         headers = {
#             'Accept': 'application/json'
#         }
#         conn.request("GET", f"/api_sellers/api/debates/v2?token={token}&id_i={dialog_id}", payload, headers)
#         res = conn.getresponse()
#         if res.status == 200:
#             data = res.read()
#             return json.loads(data.decode("utf-8"))
#         else:
#             raise Exception(f"API Error: {res.status} - {res.reason}")
#     except Exception as e:
#         print(f"Error: {e}")
#         return None
#     finally:
#         conn.close()

async def get_messages(token, dialog_id):
    url = f"https://seller.ggsel.net/api_sellers/api/debates/v2?token={token}&id_i={dialog_id}"
    headers = {"Accept": "application/json"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            # !!
            # return await response.json()

            # Обработка BOM
            raw_text = await response.text()
            text_without_bom = raw_text.encode().decode('utf-8-sig')

            return json.loads(text_without_bom)
# async def send_message(token, dialog_id, text):
#     conn = None
#     try:
#         conn = http.client.HTTPSConnection("seller.ggsel.net")
#         payload = json.dumps({
#             "message": "string"
#         })
#         headers = {
#             'Content-Type': 'application/json'
#         }
#         conn.request("POST", "/api_sellers/api/debates/v2", payload, headers)
#         res = conn.getresponse()
#         if res.status == 200:
#             data = res.read()
#             return json.loads(data.decode("utf-8"))
#         else:
#             raise Exception(f"API Error: {res.status} - {res.reason}")
#     except Exception as e:
#         print(f"Error: {e}")
#         return None
#     finally:
#         conn.close()

async def send_message(token, dialog_id, text):
    url = f"https://seller.ggsel.net/api_sellers/api/debates/v2?token={token}&id_i={dialog_id}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {"message": text}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            response.raise_for_status()
            return response.status == 200

# async def set_read_flag(token, dialog_id):
#     conn = None
#     try:
#         conn = http.client.HTTPSConnection("seller.ggsel.net")
#         headers = {
#             'Accept': 'application/json',
#             'Content-Type': 'application/json'
#         }
#         # Пробуем endpoint по аналогии со старым API
#         conn.request("POST", f"/api_sellers/api/debates/v2/seen?token={token}&id_i={dialog_id}", '', headers)
#         res = conn.getresponse()
#
#         if res.status == 200:
#             data = res.read()
#             return json.loads(data.decode("utf-8"))
#         else:
#             raise Exception(f"API Error: {res.status} - {res.reason}")
#
#     except Exception as e:
#         print(f"Error: {e}")
#         return None
#     finally:
#         if conn:
#             conn.close()


async def set_read_flag(token, dialog_id):
    url = f"https://seller.ggsel.net/api_sellers/api/debates/v2/seen?token={token}&id_i={dialog_id}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers) as response:
            response.raise_for_status()
            return response.status == 200

async def wait_for_message(token, dialog_id, message_text, customer):
    end_time = time.time() + 500

    while time.time() < end_time:
        messages = await get_messages(token, dialog_id)
        if not messages:
            print("Сообщений пока нет от пользователя!")
            await asyncio.sleep(2)
            continue

        # !! 0
        message = messages[0]

        is_buyer = message.get('buyer')
        # if message.get('message', '') and not message.get('date_seen') and is_buyer:
        if message.get('message', '') and is_buyer:
            print("Получили сообщение от пользователя!")
            return message.get('message', '')

        await asyncio.sleep(2)

    # Если время истекло и цикл завершился
    print("⏰ Время ожидания истекло!")
    customer.clicker.close_apps(token,  dialog_id, message_text, customer)
    from src.Handlers.Digiseller import tick
    await tick.finish_current_order(token, "deb")  # Вызываем метод next_order
    return None  # Возвращаем None, так как сообщение не получено


# Функции для работы с очередью
async def add_to_queue(dialog_id, customer):
    """Добавить пользователя в очередь"""
    global order_queue
    async with queue_lock:
        # Проверяем, нет ли уже этого пользователя в очереди
        for item in order_queue:
            if item[0] == dialog_id:
                return False  # Уже в очереди

        timestamp = datetime.now()
        order_queue.append((dialog_id, customer, timestamp))
        print(f"Пользователь {dialog_id} добавлен в очередь. Позиция: {len(order_queue)}")
        return True


async def get_queue_position(dialog_id):
    """Получить позицию пользователя в очереди"""
    async with queue_lock:
        for i, (queue_dialog_id, _, _) in enumerate(order_queue):
            if queue_dialog_id == dialog_id:
                return i + 1
        return None


async def get_next_customer():
    """Получить следующего клиента из очереди"""
    global order_queue
    async with queue_lock:
        if order_queue:
            return order_queue.pop(0)
        return None


async def remove_from_queue(dialog_id):
    """Убрать пользователя из очереди"""
    global order_queue
    async with queue_lock:
        order_queue = [(d_id, customer, ts) for d_id, customer, ts in order_queue if d_id != dialog_id]


async def get_estimated_wait_time(position):
    """Получить примерное время ожидания"""
    if position <= 1:
        return 0
    return (position - 1) * 10  # 10 минут на заказ

async def finish_current_order(token):
    from src.Handlers.Digiseller import tick
    await tick.finish_current_order(token, "kras")

async def notify_queue_status(token):
    """Уведомить всех в очереди о их статусе"""
    async with queue_lock:
        for i, (dialog_id, customer, timestamp) in enumerate(order_queue):
            position = i + 1
            wait_time = await get_estimated_wait_time(position)

            if position == 1:
                message = "🔥 Вы следующий в очереди! Ожидайте, скоро начнем обработку вашего заказа."
            else:
                message = f"⏳ Ваша позиция в очереди: {position}\n⏰ Примерное время ожидания: {wait_time} минут\n\n🎮 Мы обрабатываем заказы по очереди, среднее время выполнения одного заказа - 10 минут."

            try:
                await send_message(token, dialog_id, message)
            except Exception as e:
                print(f"Ошибка отправки уведомления пользователю {dialog_id}: {e}")


# Функции загрузки файлов (с обработкой ошибок)
async def upload_screenshot(token: str, screenshot_path: str, lang: str = "ru-RU") -> Optional[dict]:
    """
    Предварительная загрузка скриншота на сервер Digiseller
    """
    url = f"https://seller.ggsel.net/api_sellers/api/debates/v2/upload-preview?token={token}&lang={lang}"

    if not os.path.exists(screenshot_path):
        raise FileNotFoundError(f"Файл не найден: {screenshot_path}")

    headers = {
        "Accept": "application/json"
    }

    # Для multipart запросов используем стандартный подход с повторами
    for attempt in range(5):
        try:
            async with aiohttp.ClientSession() as session:
                with open(screenshot_path, 'rb') as file:
                    form_data = aiohttp.FormData()
                    form_data.add_field('file', file,
                                        filename=os.path.basename(screenshot_path),
                                        content_type='image/png')

                    async with session.post(url, headers=headers, data=form_data) as response:
                        if response.status in {429, 502}:
                            wait_time = 2 ** attempt
                            print(f"Ошибка {response.status} при загрузке файла. Ждем {wait_time}s")
                            await asyncio.sleep(wait_time)
                            continue
                        response.raise_for_status()
                        return await response.json()
        except Exception as e:
            if attempt < 4:
                wait_time = 2 ** attempt
                print(f"Ошибка загрузки файла: {e}. Повтор через {wait_time}s")
                await asyncio.sleep(wait_time)
                continue
            raise

    raise Exception("Не удалось загрузить файл после нескольких попыток")


async def send_screenshot(token, dialog_id, message_text, customer):
    # Делаем скриншот
    screenshot = pyautogui.screenshot()
    temp_path = "gta_screen.png"
    final_path = r"D:\Repos\gta_screen.png"

    # Сохраняем временно
    screenshot.save(temp_path)

    # Сжимаем
    compress_image(temp_path, final_path, max_size_kb=4500)

    # Отправляем
    success = await send_screenshot_message(token, dialog_id, message_text, final_path)

    # Удаляем временные файлы
    try:
        os.remove(temp_path)
        os.remove(final_path)
    except:
        pass

    return success


async def send_screenshot_message(token: str, dialog_id: str, message_text: str,
                                  screenshot_path: str, lang: str = "ru-RU") -> bool:
    """
    Отправка сообщения со скриншотом пользователю Digiseller
    """
    try:
        # Шаг 1: Предварительная загрузка скриншота
        upload_response = False #await upload_screenshot(token, screenshot_path, lang)

        if not upload_response:
            print("Ошибка загрузки файла")
            return False

        # Логирование ответа загрузки
        print(f"Upload response: {upload_response}")

        # Проверяем структуру ответа
        if "files" not in upload_response or not upload_response["files"]:
            print(f"Неверный формат ответа загрузки: {upload_response}")
            return False

        file_info = upload_response["files"][0]

        # Проверяем обязательные поля
        required_fields = ["newid", "name", "type", "size"]
        for field in required_fields:
            if field not in file_info:
                print(f"Отсутствует обязательное поле: {field}")
                return False

        url = f"https://seller.ggsel.net/api_sellers/api/debates/v2?token={token}&id_i={dialog_id}"

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        # Формируем payload согласно документации
        payload = {
            "files": [{
                "newid": file_info["newid"],
                "name": file_info["name"],
                "type": file_info["type"],
                "size": file_info["size"]
            }]
        }

        print(f"Sending to URL: {url}")
        print(f"Payload: {payload}")

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                response_text = await response.text()
                print(f"Response status: {response.status}, body: {response_text}")

                response.raise_for_status()
                # Согласно документации, пустой ответ с кодом 200 означает успех
                return response.status == 200

    except aiohttp.ClientResponseError as e:
        print(f"Ошибка отправки скриншота: {e.status}, message='{e.message}', url='{e.request_info.url}'")
        return False
    except Exception as e:
        print(f"Ошибка отправки скриншота: {e}")
        return False


def compress_image(input_path, output_path, max_size_kb=4500):
    """
    Сжимает изображение до указанного размера в KB
    """
    img = Image.open(input_path)

    # Начальное качество
    quality = 85

    while True:
        img.save(output_path, "PNG", optimize=True, quality=quality)
        size_kb = os.path.getsize(output_path) / 1024

        if size_kb <= max_size_kb or quality <= 20:
            break

        quality -= 5

    print(f"Сжато до {size_kb:.1f} KB с качеством {quality}")
    return output_path


async def get_purchase_info(token: str, invoice_id: int) -> Optional[dict]:
    """
    Получение информации о продаже по номеру заказа

    Args:
        token: Токен авторизации API Digiseller
        invoice_id: Номер счета/заказа (ID инвойса)

    Returns:
        dict: Информация о заказе в формате JSON
        None: В случае ошибки

    Raises:
        aiohttp.ClientResponseError: При ошибках HTTP запроса
    """
    url = f"https://seller.ggsel.net/api_sellers/api/purchase/info/{invoice_id}?token={token}"

    headers = {
        "Accept": "application/json"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                return await response.json()

    except aiohttp.ClientResponseError as e:
        print(f"Ошибка получения информации о заказе {invoice_id}: {e.status}, message='{e.message}'")
        return None

    except Exception as e:
        print(f"Ошибка получения информации о заказе {invoice_id}: {e}")
        return None


async def get_all_sales(token: str, product_ids: Optional[str] = None,
                        max_pages: int = 10) -> list:
    """
    Получение всех продаж постранично

    Args:
        token: Токен авторизации API
        product_ids: ID товаров через запятую (опционально)
        max_pages: Максимальное количество страниц для загрузки

    Returns:
        list: Список всех продаж
    """
    all_sales = []
    page = 1

    while page <= max_pages:
        sales_data = await get_last_sales(token, product_ids=product_ids, page=page, rows=1000)

        if not sales_data or not sales_data.get('rows'):
            break

        all_sales.extend(sales_data['rows'])

        # Проверяем, есть ли еще страницы
        total_count = sales_data.get('cnt_all', 0)
        if len(all_sales) >= total_count:
            break

        page += 1

        # Небольшая задержка между запросами
        await asyncio.sleep(0.5)

    return all_sales


async def get_last_sales(token: str,
                         seller_id: int = 0,
                         top: int = 20,
                         group: str = "true") -> Optional[dict]:
    """
    Получение списка последних продаж

    Args:
        token: Токен авторизации API Digiseller
        seller_id: ID продавца (по умолчанию 0)
        top: Количество записей (по умолчанию 1000)
        group: Группировка "true" или "false" (по умолчанию "true")

    Returns:
        dict: Список последних продаж
        None: В случае ошибки
    """
    url = "https://seller.ggsel.net/api_sellers/api/seller-last-sales"

    headers = {
        "Accept": "application/json"
    }

    # Формируем параметры согласно документации
    params = {
        "seller_id": seller_id,
        "top": top,
        "group": group,
        "token": token
    }

    try:
        async with aiohttp.ClientSession() as session:#, params=params
            async with session.get(url, headers=headers) as response:
                # Логирование для отладки
                print(f"Request URL: {response.url}")

                response.raise_for_status()
                data = await response.json()

                # Проверяем код возврата
                if data.get("retval") != 0:
                    print(f"API ошибка: {data.get('retdesc')}")
                    return None

                return data

    except aiohttp.ClientResponseError as e:
        print(f"HTTP ошибка {e.status}: {e.message}")
        print(f"URL: {e.request_info.url}")
        return None

    except Exception as e:
        print(f"Ошибка: {e}")
        return None


async def check_new_sales(token: str) -> list:
    """
    Проверяет наличие новых продаж и возвращает список новых
# id = dialogs['chats'][3]['id_i']
# info = await get_purchase_info(token, id)
    Returns:
        list: Список новых продаж [{sale_data}, ...]
    """
    global processed_sales

    # Получаем последние продажи
    sales_data = await get_last_sales(token, seller_id=SELLER_ID, top=customers_count)

    if not sales_data or not sales_data.get('sales'):
        return []

    new_sales = []

    for sale in sales_data['sales']:
        # Создаем уникальный ID продажи (дата + product_id)
        sale_date = sale.get('date', '')
        product_id = sale.get('product', {}).get('id')

        # Если продажа еще не обработана
        if product_id not in processed_sales:
            new_sales.append(sale)
            processed_sales.add(product_id)
            print(f"🆕 Обнаружена новая продажа: {product_id}")

    return new_sales


async def get_dialog_id_from_sale(token: str, ids: int) -> Optional[str]:
    """
    Получает dialog_id из данных продажи

    Args:
        token: Токен API
        ids: Данные продажи

    Returns:
        str: dialog_id или None
    """
    # Если в данных продажи есть invoice_id, получаем информацию о покупке
    invoice_id = ids

    if invoice_id:
        purchase_info = await get_purchase_info(token, invoice_id)
        if purchase_info:
            # Ищем dialog_id в информации о покупке
            # (структура может отличаться, проверьте API документацию)
            return purchase_info.get('dialog_id')

    return None
