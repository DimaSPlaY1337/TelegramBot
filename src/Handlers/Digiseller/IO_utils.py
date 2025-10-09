# import asyncio
# import os
#
# import aiohttp
# import hashlib
# import time
# from typing import Optional
#
# API_KEY = "DA4D6D5B237C4EA1974F0815AB890849"
# SELLER_ID = 889983
#
#
# async def get_token():
#     url = "https://api.digiseller.com/api/apilogin"
#     timestamp = int(time.time())
#     sign_source = f"{API_KEY}{timestamp}"
#     sign = hashlib.sha256(sign_source.encode()).hexdigest()
#     payload = {
#         "seller_id": SELLER_ID,
#         "timestamp": timestamp,
#         "sign": sign
#     }
#     headers = {
#         "Content-Type": "application/json",
#         "Accept": "application/json"
#     }
#     async with aiohttp.ClientSession() as session:
#         async with session.post(url, headers=headers, json=payload) as response:
#             response.raise_for_status()
#             data = await response.json()
#             return data["token"]
#
# async def get_dialogs(token):
#     url = f"https://api.digiseller.com/api/debates/v2/chats?token={token}"
#     headers = {"Accept": "application/json"}
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url, headers=headers) as response:
#             response.raise_for_status()
#             return await response.json()
#
# async def wait_for_message(token, dialog_id):
#     while True:
#         messages = await get_messages(token, dialog_id)
#
#         if not messages:
#             print("Сообщений пока нет от пользователя!")
#             await asyncio.sleep(2)
#             continue
#
#         message = messages[-1]
#         if message.get('message', '') and not message.get('date_seen') and message.get('buyer'):
#             print("Получили сообщение от пользователя!")
#             return message.get('message', '')
#         await asyncio.sleep(2)
#
# async def get_messages(token, dialog_id):
#     url = f"https://api.digiseller.com/api/debates/v2?token={token}&id_i={dialog_id}"
#     headers = {"Accept": "application/json"}
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url, headers=headers) as response:
#             response.raise_for_status()
#             return await response.json()
#
# async def send_message(token, dialog_id, text):
#     url = f"https://api.digiseller.com/api/debates/v2/?token={token}&id_i={dialog_id}"
#     headers = {
#         "Accept": "application/json",
#         "Content-Type": "application/json"
#     }
#     payload = {"message": text}
#     async with aiohttp.ClientSession() as session:
#         async with session.post(url, headers=headers, json=payload) as response:
#             response.raise_for_status()
#             return response.status == 200
#
# async def set_read_flag(token, dialog_id):
#     url = f"https://api.digiseller.com/api/debates/v2/seen?token={token}&id_i={dialog_id}"
#     headers = {
#         "Accept": "application/json",
#         "Content-Type": "application/json"
#     }
#     async with aiohttp.ClientSession() as session:
#         async with session.post(url, headers=headers) as response:
#             response.raise_for_status()
#             return response.status == 200
#
#
# async def upload_screenshot(token: str, screenshot_path: str, lang: str = "ru-RU") -> Optional[dict]:
#     """
#     Предварительная загрузка скриншота на сервер Digiseller
#     """
#     url = f"https://api.digiseller.com/api/debates/v2/upload-preview?token={token}&lang={lang}"
#
#     if not os.path.exists(screenshot_path):
#         raise FileNotFoundError(f"Файл не найден: {screenshot_path}")
#
#     headers = {
#         "Accept": "application/json"
#     }
#
#     async with aiohttp.ClientSession() as session:
#         with open(screenshot_path, 'rb') as file:
#             form_data = aiohttp.FormData()
#             form_data.add_field('file', file,
#                                 filename=os.path.basename(screenshot_path),
#                                 content_type='image/png')
#
#             async with session.post(url, headers=headers, data=form_data) as response:
#                 response.raise_for_status()
#                 return await response.json()
#
#
# async def send_screenshot_message(token: str, dialog_id: str, message_text: str,
#                                   screenshot_path: str, lang: str = "ru-RU") -> bool:
#     """
#     Отправка сообщения со скриншотом пользователю Digiseller
#     """
#     try:
#         # Шаг 1: Предварительная загрузка скриншота
#         upload_response = await upload_screenshot(token, screenshot_path, lang)
#
#         if not upload_response:
#             print("Ошибка загрузки файла")
#             return False
#
#         # Шаг 2: Отправка сообщения с файлом
#         url = f"https://api.digiseller.com/api/debates/v2/?token={token}&id_i={dialog_id}"
#         headers = {
#             "Accept": "application/json",
#             "Content-Type": "application/json"
#         }
#
#         # Формируем payload с текстом и информацией о файле
#         payload = {
#             "message": message_text,
#             "files": [{
#                 "newid": upload_response.get("files", [{}])[0].get("newid"),
#                 "name": upload_response.get("files", [{}])[0].get("name"),
#                 "type": upload_response.get("files", [{}])[0].get("type"),
#                 "size": upload_response.get("files", [{}])[0].get("size")
#             }]
#         }
#
#         async with aiohttp.ClientSession() as session:
#             async with session.post(url, headers=headers, json=payload) as response:
#                 response.raise_for_status()
#                 return response.status == 200
#
#     except Exception as e:
#         print(f"Ошибка отправки скриншота: {e}")
#         return False
#
# from datetime import datetime
# queue_lock = asyncio.Lock()  # ?
# order_queue = []
# current_processing = None
# async def add_to_queue(dialog_id, customer):
#     """Добавить пользователя в очередь"""
#     global order_queue
#     async with queue_lock:
#         # Проверяем, нет ли уже этого пользователя в очереди
#         for item in order_queue:
#             if item[0] == dialog_id:
#                 return False  # Уже в очереди
#
#         timestamp = datetime.now()
#         order_queue.append((dialog_id, customer, timestamp))
#         print(f"Пользователь {dialog_id} добавлен в очередь. Позиция: {len(order_queue)}")
#         return True
#
# async def get_queue_position(dialog_id):
#     """Получить позицию пользователя в очереди"""
#     async with queue_lock:
#         for i, (queue_dialog_id, _, _) in enumerate(order_queue):
#             if queue_dialog_id == dialog_id:
#                 return i + 1
#         return None
import asyncio
import ctypes
import os
import aiohttp
import hashlib
import time
from datetime import datetime
from typing import Optional

import pyautogui
from PIL import Image

API_KEY = "DA4D6D5B237C4EA1974F0815AB890849"
SELLER_ID = 889983

# Система очереди
order_queue = []  # Очередь заказов [(dialog_id, customer, timestamp)]
current_processing = None  # Текущий обрабатываемый заказ
queue_lock = asyncio.Lock()#?


# Обработка ошибок 429/502
# async def request_with_retries(method, url, session, max_retries=5, retry_statuses={429, 502}, **kwargs):
#     """
#     Универсальная функция для HTTP-запросов с повторными попытками при 429/502 ошибках
#     """
#     for attempt in range(max_retries):
#         try:
#             async with getattr(session, method)(url, **kwargs) as response:
#                 if response.status in retry_statuses:
#                     wait_time = 2 ** attempt  # экспоненциальная задержка
#                     print(
#                         f"Получена ошибка {response.status} для {url}. Ждем {wait_time}s перед повтором (попытка {attempt + 1}/{max_retries})")
#                     await asyncio.sleep(wait_time)
#                     continue
#                 response.raise_for_status()
#                 return await response.json()
#         except aiohttp.ClientResponseError as e:
#             if e.status in retry_statuses and attempt < max_retries - 1:
#                 wait_time = 2 ** attempt
#                 print(
#                     f"ClientResponseError {e.status} для {url}. Ждем {wait_time}s перед повтором (попытка {attempt + 1}/{max_retries})")
#                 await asyncio.sleep(wait_time)
#                 continue
#             raise
#         except Exception as e:
#             if attempt < max_retries - 1:
#                 wait_time = 2 ** attempt
#                 print(
#                     f"Неожиданная ошибка для {url}: {e}. Ждем {wait_time}s перед повтором (попытка {attempt + 1}/{max_retries})")
#                 await asyncio.sleep(wait_time)
#                 continue
#             raise
#
#     raise Exception(f"Превышено максимальное количество попыток для {url}")
async def get_token():
    url = "https://api.digiseller.com/api/apilogin"
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

async def get_dialogs(token):
    url = f"https://api.digiseller.com/api/debates/v2/chats?token={token}"
    headers = {"Accept": "application/json"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            return await response.json()

async def get_messages(token, dialog_id):
    url = f"https://api.digiseller.com/api/debates/v2?token={token}&id_i={dialog_id}"
    headers = {"Accept": "application/json"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            return await response.json()

async def send_message(token, dialog_id, text):
    url = f"https://api.digiseller.com/api/debates/v2/?token={token}&id_i={dialog_id}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {"message": text}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            response.raise_for_status()
            return response.status == 200

# async def request_with_retries_post(method, url, session, max_retries=5, retry_statuses={429, 502}, **kwargs):
#     """
#     Универсальная функция для POST-запросов с повторными попытками при 429/502 ошибках
#     Возвращает True при успехе, не пытается декодировать JSON
#     """
#     for attempt in range(max_retries):
#         try:
#             async with getattr(session, method)(url, **kwargs) as response:
#                 if response.status in retry_statuses:
#                     wait_time = 2 ** attempt  # экспоненциальная задержка
#                     print(
#                         f"Получена ошибка {response.status} для {url}. Ждем {wait_time}s перед повтором (попытка {attempt + 1}/{max_retries})")
#                     await asyncio.sleep(wait_time)
#                     continue
#                 response.raise_for_status()
#                 # Пытаемся получить JSON, если не получается - возвращаем True
#                 try:
#                     return await response.json()
#                 except aiohttp.ContentTypeError:
#                     # Сервер вернул не JSON (например, пустой ответ или текст)
#                     return True
#         except aiohttp.ClientResponseError as e:
#             if e.status in retry_statuses and attempt < max_retries - 1:
#                 wait_time = 2 ** attempt
#                 print(
#                     f"ClientResponseError {e.status} для {url}. Ждем {wait_time}s перед повтором (попытка {attempt + 1}/{max_retries})")
#                 await asyncio.sleep(wait_time)
#                 continue
#             raise
#         except Exception as e:
#             if attempt < max_retries - 1:
#                 wait_time = 2 ** attempt
#                 print(
#                     f"Неожиданная ошибка для {url}: {e}. Ждем {wait_time}s перед повтором (попытка {attempt + 1}/{max_retries})")
#                 await asyncio.sleep(wait_time)
#                 continue
#             raise
#
#     raise Exception(f"Превышено максимальное количество попыток для {url}")

async def set_read_flag(token, dialog_id):
    url = f"https://api.digiseller.com/api/debates/v2/seen?token={token}&id_i={dialog_id}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers) as response:
            response.raise_for_status()
            return response.status == 200

async def wait_for_message(token, dialog_id):
    while True:
        messages = await get_messages(token, dialog_id)
        if not messages:
            print("Сообщений пока нет от пользователя!")
            await asyncio.sleep(2)
            continue

        message = messages[-1]
        if message.get('message', '') and not message.get('date_seen') and message.get('buyer'):
            print("Получили сообщение от пользователя!")
            return message.get('message', '')

        await asyncio.sleep(2)


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
    await finish_current_order(token)

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
    url = f"https://api.digiseller.com/api/debates/v2/upload-preview?token={token}&lang={lang}"

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


def set_numlock_state(state):
    """Включает/выключает NumLock"""
    VK_NUMLOCK = 0x90
    KEYEVENTF_EXTENDEDKEY = 0x0001
    KEYEVENTF_KEYUP = 0x0002

    user32 = ctypes.windll.user32

    # Получаем текущее состояние NumLock
    current_state = user32.GetKeyState(VK_NUMLOCK) & 1

    if current_state != state:
        # Имитируем нажатие NumLock
        user32.keybd_event(VK_NUMLOCK, 0, KEYEVENTF_EXTENDEDKEY, 0)
        user32.keybd_event(VK_NUMLOCK, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0)


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
        upload_response = await upload_screenshot(token, screenshot_path, lang)

        if not upload_response:
            print("Ошибка загрузки файла")
            return False

        # Шаг 2: Отправка сообщения с файлом
        url = f"https://api.digiseller.com/api/debates/v2/?token={token}&id_i={dialog_id}"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        # Формируем payload с текстом и информацией о файле
        payload = {
            "message": message_text,
            "files": [{
                "newid": upload_response.get("files", [{}])[0].get("newid"),
                "name": upload_response.get("files", [{}])[0].get("name"),
                "type": upload_response.get("files", [{}])[0].get("type"),
                "size": upload_response.get("files", [{}])[0].get("size")
            }]
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                response.raise_for_status()
                return response.status == 200

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