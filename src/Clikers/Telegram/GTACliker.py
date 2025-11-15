from src.Clikers.Telegram.input_utils import *
from src.common import bot
import src.common as common
from src.Handlers.Telegram.rules import error_handler
import traceback

async def gta_cliker_exp(message):
    """GTA Clicker для расширенной версии"""
    try:
        print("Кликер начал работу")
        chat_id = message.chat.id
        customer = common.get_customer(chat_id)
        keyboard = Controller()

        # Последовательность команд
        press_key('f5')
        press_key('down', 4)

        # Обработка денег
        if customer.order_des["amount"].isdigit():
            press_key('enter')
            press_key('enter')
            press_key('enter')
            press_key('down', 1)
            press_key('enter')

            sum_amount = int(customer.order_des["amount"])
            if sum_amount < 7000000:
                sum_amount = 7000000

            order = 75000000
            if sum_amount < order:
                order = sum_amount

            keyboard.type(str(order))
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            press_key('enter')
            time.sleep(0.5)

            press_key('down')
            press_key('enter')

            result = str(sum_amount - order)
            keyboard.type(result)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            time.sleep(0.5)

            press_key('backspace')
            press_key('down', 5)
            press_key('enter')
            time.sleep(1)

            # Ожидание изменения цвета
            x = 2405
            y = 798
            while True:
                r, g, b = pyautogui.pixel(x, y)
                print(f"Текущий цвет: {r}, {g}, {b}")
                if not await is_red(r, g, b):
                    print("Цвет стал целевым!")
                    break
                time.sleep(0.2)

            press_key('up', 4)
            press_key('enter')
            press_key('enter')

            x = 2404
            y = 567
            r, g, b = pyautogui.pixel(x, y)

            while await is_red(r, g, b):
                r, g, b = pyautogui.pixel(x, y)
                print(f"Текущий цвет: {r}, {g}, {b}")
                print("Цвет стал целевым!")

            press_key('backspace')
            press_key('backspace')

        # Обработка уровней
        press_key('down', 2)
        press_key('enter')

        if customer.order_des["levels"].isdigit():
            order = int(customer.order_des["levels"])
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            time.sleep(0.5)
            write_text(order, 0.2)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            time.sleep(0.5)

            press_key('down')
            press_key('enter')
            time.sleep(10)
            press_key('backspace')

        # Обработка unlocks
        press_key('down', 2)
        press_key('enter')
        press_key('up', 1)
        press_key('enter')

        if customer.order_des["unlocks"].lower() == "standard unlocks":
            press_key('enter')
        elif customer.order_des["unlocks"].lower() == "super unlocks":
            press_key('down', 1)
            press_key('enter')

        time.sleep(10)

        # Завершение
        switch_to_english()
        press_key('o')
        time.sleep(10)
        press_key('backspace')
        press_key('backspace')
        press_key('down', 4)
        press_key('enter')
        press_key('up')
        press_key('enter')
        time.sleep(10)

        # Скриншот
        press_key('f5')
        switch_to_english()
        time.sleep(1.5)
        keyboard_press_key('z')
        time.sleep(1)
        print("Кликер закончил работу")
        await send_screens(message)
    except Exception as e:
        print(f"Ошибка в gta_cliker_exp: {e}")
        print(traceback.format_exc())
        await error_handler(message.chat.id, traceback.format_exc())


async def send_screens(message):
    """Отправка скриншотов в Telegram"""
    try:
        chat_id = message.chat.id
        customer = common.get_customer(chat_id)

        # Делаем скриншот
        screenshot = pyautogui.screenshot()
        screenshot_path = 'gta_screen.png'
        screenshot.save(screenshot_path)

        # Отправляем в телеграм
        with open(screenshot_path, 'rb') as photo:
            await bot.send_photo(chat_id, photo, caption="✅ Работа выполнена!")

        # Закрываем приложения
        if customer.clicker:
            await customer.clicker.close_apps(message)
    except Exception as e:
        print(f"Ошибка в send_screens: {e}")
        print(traceback.format_exc())
        await error_handler(message.chat.id, traceback.format_exc())