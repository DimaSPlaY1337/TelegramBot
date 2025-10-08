from src.Clikers.Digiseller.input_utils import *
import pyautogui
import time
from pynput.keyboard import Controller, Key

from src.Handlers.Digiseller.IO_utils import send_screenshot_message


async def gta_cliker_free(customer):
    press_key("num1")

async def gta_cliker_exp(token, dialog_id, message_text, customer):
    keyboard = Controller()
    # Последовательность команд (по сообщениям)
    # f5
    press_key('f5')

    # 4 down
    press_key('down', 4)

    # write order
    if customer.order_des["amount"].isdigit():
        # enter
        press_key('enter')

        # enter
        press_key('enter')

        # galka
        press_key('enter')

        # 1 down
        press_key('down', 1)
        press_key('enter')

        sum = int(customer.order_des["amount"])
        if sum < 7000000:
            sum = 7000000

        order = 75000000
        if sum < order:
            order = sum

        keyboard.type(str(order))
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        press_key('enter')

        time.sleep(0.5)

        # down
        press_key('down')
        press_key('enter')

        # write(200000000-75000000)
        result = str(sum - order)
        keyboard.type(result)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

        time.sleep(0.5)

        # backspace
        press_key('backspace')

        # Medium safe
        press_key('down', 5)
        r, g, b = pyautogui.pixel(2305, 798)
        while not await is_gray(r,g,b):
            press_key('down')
        press_key('enter')

        time.sleep(1)
        x = 2405
        y = 798
        while True:
            # Считываем цвет пикселя
            r,g,b = pyautogui.pixel(x, y)
            print(f"Текущий цвет: {r}, {g}, {b}")

            # Проверка цвета
            if not await is_red(r,g,b):
                print("Цвет стал целевым!")
                break

        time.sleep(0.2)  # небольшая задержка, чтобы не грузить процессор
        # check red label disapear, while lable != black: wait
        # (Это требует проверки содержимого экрана, не реализовано простым pyautogui)

        # 4 up
        press_key('up', 4)

        # Казино -> Зациклить
        press_key('enter')
        press_key('enter')
        x = 2404
        y = 567

        r, g, b = pyautogui.pixel(x, y)
        while await is_red(r,g,b):
            # Считываем цвет пикселя
            r, g, b = pyautogui.pixel(x, y)
            print(f"Текущий цвет: {r}, {g}, {b}")
        print("Цвет стал целевым!")


        # backspace
        press_key('backspace')
        press_key('backspace')

    # 2 down
    press_key('down', 2)
    press_key('enter')

    # write level
    if customer.order_des["levels"].isdigit():
        order = int(customer.order_des["levels"])
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        time.sleep(0.5)
        write_text(order, 0.2)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        time.sleep(0.5)
        # 1 down
        press_key('down')
        press_key('enter')

        time.sleep(10)

    # backspace
    press_key('backspace')

    # down 2
    press_key('down', 2)
    press_key('enter')

    # up 1
    press_key('up', 1)
    press_key('enter')

    if customer.order_des["unlocks"] == "Standard Unlocks":
        press_key('enter')
    elif customer.order_des["unlocks"] == "Super Unlocks":
        press_key('down', 1)
        press_key('enter')

    time.sleep(10)
    # clava "o"
    switch_to_english()
    press_key('o')

    # 15 сек ждем
    time.sleep(10)

    # backspace
    press_key('backspace')
    press_key('backspace')

    # 8 up
    press_key('down', 4)
    press_key('enter')

    # 1 up for legacy
    press_key('up')
    press_key('enter')

    time.sleep(10)

    # делаем скриншот
    press_key('f5')
    switch_to_english()
    time.sleep(1.5)
    keyboard_press_key('z')
    # Скрин окна GTA:
    screenshot = pyautogui.screenshot()
    screenshot.save('gta_screen.png')
    time.sleep(1)
    await send_screenshot(token, dialog_id, message_text, customer)

async def send_screenshot(token, dialog_id, message_text, customer):
    await send_screenshot_message(token, dialog_id, message_text, r"D:\Repos\gta_screen.png")
    await customer.clicker.close_apps()