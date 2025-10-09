# import aiohttp
# import asyncio
#
# from src.Handlers.Digiseller.IO_utils import get_token, add_to_queue, get_queue_position, send_message, \
#     current_processing
# from DigisellersWelcome import send_welcome, customers
# from ChoosingPlatform import (
#     handle_platform_choice, handle_login, handle_password, handle_version
# )
# from OrderDesc import (
#     handle_order_choice, handle_money_input, handle_levels_input,
#     handle_unlocks_input, handle_order_continue, check_order_completion
# )
#
#
# async def get_dialogs(token):
#     url = f"https://api.digiseller.com/api/debates/v2/chats?token={token}"
#     headers = {"Accept": "application/json"}
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url, headers=headers) as response:
#             response.raise_for_status()
#             return await response.json()
#
#
# async def get_messages(token, dialog_id):
#     url = f"https://api.digiseller.com/api/debates/v2?token={token}&id_i={dialog_id}"
#     headers = {"Accept": "application/json"}
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url, headers=headers) as response:
#             response.raise_for_status()
#             return await response.json()
#
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
# async def handle_dialog(token, dialog):
#     dialog_id = dialog['id_i']
#     messages = await get_messages(token, dialog_id)
#
#     for message in reversed(messages):  # Обрабатываем с самых новых
#         text = message.get('message', '').lower()
#
#         s = message.get('buyer')
#         if not message.get('date_seen') and s:  # Только непрочитанные
#             customer = customers.get(dialog_id)
#
#             if "start" in text:
#                 await send_welcome(token, dialog_id, message)
#                 await set_read_flag(token, dialog_id)
#                 break
#             elif customer:
#                 await process_message_by_step(token, dialog_id, message.get('message', ''), customer)
#                 await set_read_flag(token, dialog_id)
#                 break
#         else:
#             break
#     #     dialog_id = dialog['id_i']
#     #     messages = await get_messages(token, dialog_id)
#     #
#     #     for message in reversed(messages):  # Обрабатываем с самых новых
#     #         text = message.get('message', '').lower()
#     #         is_buyer = message.get('buyer')
#     #
#     #         if not message.get('date_seen') and is_buyer:  # Только непрочитанные от покупателей
#     #             customer = customers.get(dialog_id)
#     #
#     #             if "start" in text and not customer:
#     #                 # Новый клиент написал start
#     #                 print(f"Новый клиент {dialog_id} написал 'start'")
#     #
#     #                 # Создаем временного клиента для очереди (или получаем из send_welcome)
#     #                 await send_welcome(token, dialog_id, message)
#     #                 customer = customers.get(dialog_id)
#     #
#     #                 if customer:
#     #                     # Добавляем в очередь
#     #                     added = await add_to_queue(dialog_id, customer)
#     #                     if added:
#     #                         position = await get_queue_position(dialog_id)
#     #                         if position == 1:
#     #                             await send_message(token, dialog_id,
#     #                                                "🎮 Добро пожаловать! Вы первый в очереди, начинаем обработку вашего заказа прямо сейчас!")
#     #                         else:
#     #                             wait_time = (position - 1) * 10
#     #                             await send_message(token, dialog_id,
#     #                                                f"🎮 Добро пожаловать! Вы добавлены в очередь.\n\n"
#     #                                                f"📍 Ваша позиция: {position}\n"
#     #                                                f"⏰ Примерное время ожидания: {wait_time} минут\n\n"
#     #                                                f"⚡ Мы обрабатываем заказы последовательно, среднее время выполнения одного заказа - 10 минут.")
#     #
#     #                     await set_read_flag(token, dialog_id)
#     #                 break
#     #
#     #             # Если клиент уже есть, но не в процессе обработки - проверяем очередь
#     #             elif customer and dialog_id != current_processing:
#     #                 position = await get_queue_position(dialog_id)
#     #                 if position is not None:
#     #                     # Клиент в очереди написал сообщение
#     #                     await send_message(token, dialog_id,
#     #                                        f"⏳ Ваше сообщение получено. Вы в очереди на позиции {position}.\n"
#     #                                        f"⏰ Ожидаемое время: {(position - 1) * 10} минут. Пожалуйста, ожидайте.")
#     #                     await set_read_flag(token, dialog_id)
#     #                 break
#
#
# async def process_message_by_step(token, dialog_id, message_text, customer):
#     step = customer.user_step
#     message_text_ls = message_text.lower().strip()
#
#     if step == "choose_platform":
#         await handle_platform_choice(token, dialog_id, message_text_ls, customer)
#     elif step == "login":
#         await handle_login(token, dialog_id, message_text, customer)
#     elif step == "password":
#         await handle_password(token, dialog_id, message_text, customer)
#     elif step == "version_of_game":
#         await handle_version(token, dialog_id, message_text_ls, customer)
#     elif step == "order_des":
#         await handle_order_choice(token, dialog_id, message_text_ls, customer)
#     elif step == "money":
#         await handle_money_input(token, dialog_id, message_text_ls, customer)
#     elif step == "levels":
#         await handle_levels_input(token, dialog_id, message_text_ls, customer)
#     elif step == "unlocks":
#         await handle_unlocks_input(token, dialog_id, message_text_ls, customer)
#     elif step == "order_con":
#         await handle_order_continue(token, dialog_id, message_text_ls, customer)
#     elif step == "rock_steam_guard":
#         await customer.clicker.rockstar_cliker(token, dialog_id, message_text_ls, customer)
#     elif step == "steam_guard":
#         await customer.clicker.plat_guard(token, dialog_id, message_text_ls, customer)
#
#
# async def reply_to_customers():
#     token = await get_token()
#     dialogs = await get_dialogs(token)
#     dialog_list = dialogs["chats"]
#     batch_size = 3
#
#     for i in range(0, len(dialog_list), batch_size):
#         batch = dialog_list[i:i + batch_size]
#         for dialog in batch:
#             print(dialog)
#         print("---------------------------------------------------")
#         tasks = [asyncio.create_task(handle_dialog(token, dialog)) for dialog in batch]
#         await asyncio.gather(*tasks)
#
#
# async def main():
#     while True:
#         try:
#             await reply_to_customers()
#         except Exception as e:
#             print("Ошибка:", e)
#         await asyncio.sleep(1)  # Опрос каждые 5 секунд
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
import asyncio

from src.Clikers.Digiseller.input_utils import find_dynamic_window
from src.Handlers.Digiseller.IO_utils import (
    get_token, get_messages, send_message, set_read_flag,
    add_to_queue, get_queue_position, get_next_customer,
    remove_from_queue, notify_queue_status, current_processing, get_dialogs
)
from DigisellersWelcome import send_welcome, customers
from ChoosingPlatform import (
    handle_platform_choice, handle_login, handle_password, handle_version, choosing_platform
)
from OrderDesc import (
    handle_order_choice, handle_money_input, handle_levels_input,
    handle_unlocks_input, handle_order_continue, check_order_completion
)


# Обработка диалогов (теперь только сканирование, не обработка)
async def scan_dialogs_for_new_customers(token, dialog_list):
    global current_processing
    """Сканируем диалоги и добавляем новых клиентов в очередь"""
    for dialog in dialog_list:
        dialog_id = dialog['id_i']
        messages = await get_messages(token, dialog_id)

        for message in reversed(messages):  # Обрабатываем с самых новых
            text = message.get('message', '').lower()
            is_buyer = message.get('buyer')

            if not message.get('date_seen') and is_buyer:  # Только непрочитанные от покупателей
                customer = customers.get(dialog_id)

                if "start" in text and not customer:
                    # Новый клиент написал start
                    print(f"Новый клиент {dialog_id} написал 'start'")

                    # Создаем временного клиента для очереди (или получаем из send_welcome)
                    await send_welcome(token, dialog_id, message)
                    customer = customers.get(dialog_id)

                    if customer:
                        # Добавляем в очередь
                        added = await add_to_queue(dialog_id, customer)
                        if added:
                            position = await get_queue_position(dialog_id)
                            if position == 1:
                                await send_message(token, dialog_id,
                                                   "🎮 Добро пожаловать! Вы первый в очереди, начинаем обработку вашего заказа прямо сейчас!")
                                current_processing = dialog_id
                                await choosing_platform(token, dialog_id, message, customer)
                            else:
                                wait_time = (position - 1) * 10
                                await send_message(token, dialog_id,
                                                   f"🎮 Добро пожаловать! Вы добавлены в очередь.\n\n"
                                                   f"📍 Ваша позиция: {position}\n"
                                                   f"⏰ Примерное время ожидания: {wait_time} минут\n\n"
                                                   f"⚡ Мы обрабатываем заказы последовательно, среднее время выполнения одного заказа - 10 минут.")

                        await set_read_flag(token, dialog_id)
                    break

                # Если клиент уже есть, но не в процессе обработки - проверяем очередь
                elif customer and dialog_id != current_processing:
                    position = await get_queue_position(dialog_id)
                    if position is not None:
                        # Клиент в очереди написал сообщение
                        await send_message(token, dialog_id,
                                           f"⏳ Ваше сообщение получено. Вы в очереди на позиции {position}.\n"
                                           f"⏰ Ожидаемое время: {(position - 1) * 10} минут. Пожалуйста, ожидайте.")
                        await set_read_flag(token, dialog_id)
                    break


async def process_current_customer(token):
    """Обработка текущего клиента (того, кто сейчас в работе)"""
    global current_processing

    if current_processing:
        dialog_id = current_processing
        customer = customers.get(dialog_id)

        if customer:
            messages = await get_messages(token, dialog_id)

            for message in reversed(messages):
                text = message.get('message', '')
                is_buyer = message.get('buyer')

                if not message.get('date_seen') and is_buyer:
                    print(f"Обрабатываем сообщение от текущего клиента {dialog_id}: {text}")
                    await process_message_by_step(token, dialog_id, text, customer)
                    await set_read_flag(token, dialog_id)
                    break


async def process_message_by_step(token, dialog_id, message_text, customer):
    """Обработка сообщения по шагам"""
    step = customer.user_step
    message_text_ls = message_text.lower().strip()

    print(f"Обрабатываем шаг {step} для клиента {dialog_id}")

    if step == "choose_platform":
        await handle_platform_choice(token, dialog_id, message_text_ls, customer)
    elif step == "login":
        await handle_login(token, dialog_id, message_text, customer)
    elif step == "password":
        await handle_password(token, dialog_id, message_text, customer)
    elif step == "version_of_game":
        await handle_version(token, dialog_id, message_text_ls, customer)
    elif step == "order_des":
        await handle_order_choice(token, dialog_id, message_text_ls, customer)
    elif step == "money":
        await handle_money_input(token, dialog_id, message_text_ls, customer)
    elif step == "levels":
        await handle_levels_input(token, dialog_id, message_text_ls, customer)
    elif step == "unlocks":
        await handle_unlocks_input(token, dialog_id, message_text_ls, customer)
    elif step == "order_con":
        await handle_order_continue(token, dialog_id, message_text_ls, customer)
    # elif step == "rock_steam_guard":
    #     await customer.clicker.rockstar_cliker(token, dialog_id, message_text_ls, customer)
    # elif step == "steam_guard":
    #     await customer.clicker.plat_guard(token, dialog_id, message_text_ls, customer)

    # Проверяем, завершен ли заказ
    # if await check_order_completion(token, dialog_id, message_text, customer):
    #     print(f"Заказ для клиента {dialog_id} завершен")
    #     await finish_current_order(token)


async def start_next_order(token):
    """Начать следующий заказ из очереди"""
    global current_processing

    if current_processing:
        return  # Уже обрабатываем кого-то

    next_customer = await get_next_customer()
    if next_customer:
        dialog_id, customer, timestamp = next_customer
        current_processing = dialog_id

        print(f"Начинаем обработку заказа для клиента {dialog_id}")

        # Уведомляем клиента о начале обработки
        await send_message(token, dialog_id,
                           "🎮 Отлично! Теперь ваш заказ в обработке. Начинаем работу!")

        # Уведомляем остальных об обновлении очереди
        await notify_queue_status(token)


async def finish_current_order(token):
    """Завершить текущий заказ и перейти к следующему"""
    global current_processing

    if current_processing:
        dialog_id = current_processing
        await send_message(token, dialog_id,
                           "✅ Ваш заказ успешно выполнен! Спасибо за использование наших услуг!")

        # Убираем из customers если нужно
        if dialog_id in customers:
            del customers[dialog_id]

        current_processing = None
        print(f"Заказ для клиента {dialog_id} завершен")

    # Запускаем следующий заказ
    await start_next_order(token)


async def main_processing_loop():
    """Главный цикл обработки"""
    while True:
        try:
            token = await get_token()
            dialogs = await get_dialogs(token)
            dialog_list = dialogs["chats"]

            # 1. Сканируем диалоги на новых клиентов
            await scan_dialogs_for_new_customers(token, dialog_list)

            # 2. Обрабатываем текущего клиента (если есть)
            await process_current_customer(token)

            # 3. Если никого не обрабатываем, берем следующего из очереди
            # if not current_processing:
            #     await start_next_order(token)

        except Exception as e:
            print(f"Ошибка в главном цикле: {e}")

        await asyncio.sleep(3)  # Проверяем каждые 3 секунды


# Задача для периодического уведомления о статусе очереди
async def queue_notification_task():
    """Периодическое уведомление клиентов в очереди"""
    # while True:
    #     try:
    #         await asyncio.sleep(60)  # Каждую минуту
    #         token = await get_token()
    #         await notify_queue_status(token)
    #     except Exception as e:
    #         print(f"Ошибка в уведомлениях очереди: {e}")
    token = await get_token()
    await notify_queue_status(token)


async def main():
    """Запуск всех задач"""
    await asyncio.gather(
        # main_processing_loop(),
        find_dynamic_window()
        # queue_notification_task()
    )


if __name__ == "__main__":
    print("🚀 Запуск системы очереди заказов...")
    asyncio.run(main())