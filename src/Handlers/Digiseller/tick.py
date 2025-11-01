import asyncio

from src.Handlers.Digiseller.IO_utils import (
    get_token, get_messages, send_message, set_read_flag,
    add_to_queue, get_queue_position, get_next_customer,
    remove_from_queue, notify_queue_status, current_processing,
    get_dialogs, get_last_sales, SELLER_ID, get_purchase_info,
    check_new_sales, processed_sales, get_dialog_id_from_sale,
    customers_count
)
from DigisellersWelcome import add_customer, customers
from ChoosingPlatform import (
    handle_platform_choice, handle_login, handle_password, handle_version, choosing_platform
)
from OrderDesc import (
    handle_order_choice, handle_money_input, handle_levels_input,
    handle_unlocks_input, handle_order_continue, check_order_completion
)


#Обработка диалогов (теперь только сканирование, не обработка)Это метод добавляет новых пользователей в очередь
#Будет заниматься поиском новых пользователей,тк process_current_c уже занимается обработкой пользователя.
async def scan_dialogs_for_new_customers(token, dialog_list):
    global current_processing
    """Сканируем диалоги и добавляем новых клиентов в очередь"""
    #!!убрать (reversed)
    for dialog in dialog_list[:customers_count]:
        dialog_id = dialog['id_i']
        if dialog_id is not None:
            messages = await get_messages(token, dialog_id)

            # for message in reversed(messages):  # Обрабатываем с самых новых
            message= messages[0]#!! 0
            text = message.get('message', '').lower()
            is_buyer = message.get('buyer')

            if is_buyer:  # Только непрочитанные от покупателей
                #TODO убрать customers и пользоваться только order_queue. Там тоже есть id. Просто 1 слоаврь, а 2 список
                customer = customers.get(dialog_id)

                #добавляем в очередь при наличии start - убрать в релизе
                if "start" in text and not dialog_id in customers:
                    # Новый клиент написал start
                    print(f"Новый клиент {dialog_id} написал 'start'")

                    # Создаем временного клиента для очереди (или получаем из send_welcome)
                    await add_customer(token, dialog_id)
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
                        # await set_read_flag(token, dialog_id) не срабатывает
                    break

                # Если клиент уже есть, но не в процессе обработки - проверяем очередь
                elif customer and dialog_id != current_processing:
                    position = await get_queue_position(dialog_id)
                    if position is not None:
                        # Клиент в очереди написал сообщение
                        await send_message(token, dialog_id,
                                           f"⏳ Ваше сообщение получено. Вы в очереди на позиции {position}.\n"
                                           f"⏰ Ожидаемое время: {(position - 1) * 10} минут. Пожалуйста, ожидайте.")
                        # await set_read_flag(token, dialog_id) не срабатывает
                    break


async def process_current_customer(token):
    """Обработка текущего клиента (того, кто сейчас в работе)"""
    global current_processing

    if current_processing:
        dialog_id = current_processing
        customer = customers.get(dialog_id)

        if customer:
            messages = await get_messages(token, dialog_id)

            # for message in reversed(messages):
            message = messages[0]
            text = message.get('message', '')
            is_buyer = message.get('buyer')

            if not message.get('date_seen') and is_buyer:
                print(f"Обрабатываем сообщение от текущего клиента {dialog_id}: {text}")
                await process_message_by_step(token, dialog_id, text, customer)

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


async def finish_current_order(token, status):
    """Завершить текущий заказ и перейти к следующему"""
    global current_processing

    if current_processing:
        dialog_id = current_processing
        if status == "kras":
            await send_message(token, dialog_id,
                               f"✅ Готово! Спасибо за заказ — вы теперь на новом уровне 💸\n"
                                    f"Прокачка завершена — заходите в игру и наслаждайтесь результатом!\n"
                                    f"🎁 В знак благодарности — +15% валюты при следующем заказе, если вы оставите отзыв!\n"
                                    f"💬 Каждый отзыв — мощная поддержка. Спасибо, что с нами!\n"
                                    f"Фишки можно снимать по 10 млн в сутки после траты основной налички.\n"
                                    f"Снимать их можно на кассе в здании казино.")
            # Убираем из customers если нужно
            if dialog_id in customers:
                del customers[dialog_id]

            print(f"Заказ для клиента {dialog_id} завершен")
        elif status == "deb":
            await send_message(token, dialog_id,"Время ожидания истекло. Ваш заказ перемещен в конец очереди.")
            if dialog_id in customers:
                user = order_queue.pop(0)  # Удаляет и возвращает первый элемент
                order_queue.append(user)

    current_processing = None
    # Запускаем следующий заказ
    await start_next_order(token)

async def process_new_sales_loop(token):
    """Постоянно проверяет новые продажи"""
    while True:
        try:
            new_sales = await check_new_sales(token)
            if new_sales:
                print(f"📦 Найдено новых продаж: {len(new_sales)}")
                for sale in new_sales:
                    try:
                        product_id = sale['product']['id']
                        product_name = sale['product']['name']
                        date = sale['date']
                        price = sale['product'].get('price_rub', 0)
                        invoice_id = sale.get('invoice_id')
                        print(f"🛒 Новая продажа: {product_name} (ID: {product_id})")

                        if invoice_id:
                            purchase_info = await get_purchase_info(token, invoice_id)
                            warning_message = (f"‼️ ВАЖНО, прочитайте инструкцию внимательно, ошибки с вашей стороны замедлят процесс выполнения заказа ‼\\n"
                                            f"Спасибо что выбрали наш магазин.\\n"
                                            f"Ваш заказ будет выполнен ботом для накрутки.\\n"
                                            f"Бот назначит ваше место в очерерди и пришлет дальнейшие инструкции.\\n"
                                            f"До завершения работ игра и лаунчер, в котором она куплена, должны быть закрыты.\\n"
                                            f"Далее следуйте инструкциям от бота\\n")
                            welcome_message = (
                                        f"🎉 Здравствуйте!\\n\\n"
                                        f"Спасибо за покупку: {product_name}\\n"
                                        f"💰 Сумма: {price} руб.\\n\\n"
                                        f"🎮 Мы начали обработку вашего заказа!\\n"
                                        f"Напишите 'start' для начала работы."
                                    )
                            print(welcome_message)
                            print(f"dialog_id: {invoice_id}")
                            
                    except Exception as e:
                        print(f"❌ Ошибка обработки продажи: {e}")

            # Проверяем новые продажи каждые 5 минут
            await asyncio.sleep(300)
        except Exception as e:
            print(f"Ошибка в process_new_sales_loop: {e}")
            await asyncio.sleep(10)

async def scan_dialogs_loop(token):
    """Постоянно сканирует диалоги на новых клиентов"""
    while True:
        try:
            dialogs = await get_dialogs(token)
            dialog_list = dialogs["items"]
            sorted_list = sorted(dialog_list, key=lambda x: x['last_message'], reverse=True)
            await scan_dialogs_for_new_customers(token, sorted_list)

            # Проверяем диалоги каждые 3 секунды
            await asyncio.sleep(3)
        except Exception as e:
            print(f"Ошибка в scan_dialogs_loop: {e}")
            await asyncio.sleep(5)

async def process_customer_loop(token):
    """Постоянно обрабатывает текущего клиента"""
    while True:
        try:
            await process_current_customer(token)

            # Проверяем сообщения от текущего клиента каждые 2 секунды
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Ошибка в process_customer_loop: {e}")
            await asyncio.sleep(5)

async def main_processing_loop():
    token = await get_token()
    # Запускаем все три процесса параллельно
    await asyncio.gather(
        process_new_sales_loop(token),
        scan_dialogs_loop(token),
        process_customer_loop(token)
    )
            # 3. Если никого не обрабатываем, берем следующего из очереди
            # if not current_processing:
            #     await start_next_order(token)


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
        main_processing_loop(),
        # queue_notification_task()
    )


if __name__ == "__main__":
    print("🚀 Запуск системы очереди заказов...")
    asyncio.run(main())