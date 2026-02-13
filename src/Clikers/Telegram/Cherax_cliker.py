import os
import time
from pygetwindow import PyGetWindowException
from src.Clikers.Telegram.input_utils import *
import pyautogui
from pynput.keyboard import Key
from src.common import bot
import src.common as common
from src.Handlers.Telegram.rules import error_handler
import traceback
import json

async def c_cliker(message):
    """Cherax Clicker - основная функция"""
    try:
        chat_id = message.chat.id
        customer = common.get_customer(chat_id)

        os.startfile(r"C:\Users\gamePC\Desktop\CheraxLoader.exe", 'runas')
        win = await wait_for_open("Cherax Loader", 5) or \
              await find_window_by_size(900, 600, timeout=100)

        if win:
            win_top = win.top
            win_left = win.left
            time.sleep(3)

            click(x=win_left + 127, y=win_top + 175, times=1, t=2)

            if customer.order_des["version"].lower() == "enhanced":
                click(x=win_left + 83, y=win_top + 207, times=1, t=2)
                click(x=win_left + 94, y=win_top + 207, times=1, t=2)

                if customer.platform.lower() == "steam":
                    click(x=win_left + 96, y=win_top + 239, times=1, t=2)
                elif customer.platform.lower() == "rockstar":
                    click(x=win_left + 72, y=win_top + 263, times=1, t=3)

            elif customer.order_des["version"].lower() == "legacy":
                click(x=win_left + 117, y=win_top + 222, times=1, t=2)
                click(x=win_left + 94, y=win_top + 207, times=1, t=2)

                if customer.platform.lower() == "steam":
                    click(x=win_left + 99, y=win_top + 246, times=1, t=2)
                elif customer.platform.lower() == "rockstar":
                    click(x=win_left + 50, y=win_top + 305, times=1, t=3)

            click(x=win_left + 91, y=win_top + 265, times=3, t=0.2)
            time.sleep(5)

            if customer.platform.lower() == "steam":
                await customer.clicker.steam_EULA()
                await customer.clicker.rockstar_search(message, 10, True)

            win_rock = await wait_for_open("Rockstar Games Launcher", 100)

            try:
                if win_rock:
                    win_left = win_rock.left
                    win_top = win_rock.top
                    win_rock.resizeTo(1024, 600)
                    time.sleep(1)
                    win_rock.activate()
                    time.sleep(5)
                    click(x=win_left + 905, y=win_top + 395, times=1, t=3)
            except PyGetWindowException as e:
                if "Error code from Windows: 0" in str(e):
                    print("Окно успешно активировано (ложная ошибка)")
                    click(x=win_left + 905, y=win_top + 395, times=1, t=3)
                else:
                    raise e

            time.sleep(10)
            await gta_cliker(message)
    except Exception as e:
        print(f"Ошибка в c_cliker: {e}")
        print(traceback.format_exc())
        await error_handler(message.chat.id, traceback.format_exc())


async def gta_cliker(message):
    """GTA Clicker для Cherax"""
    try:
        chat_id = message.chat.id
        customer = common.get_customer(chat_id)

        win_cherax = await wait_for_open("Cherax Loader", 5) or \
                     await find_window_by_size(900, 600, timeout=100)
        win_g = await wait_for_open("Google Chrome", 20)
        win_c = await wait_for_open("Console Window Host", 10)

        if win_cherax:
            win_cherax.minimize()
            print("Скрыли cherax")

        if win_g:
            win_g.minimize()
            print("Скрыли google")

        if win_c:
            win_c.minimize()
            print("Console Window Host")

        if customer.order_des["version"].lower() == "enhanced":
            time.sleep(2)
            found = False
            end_time = time.time() + 30

            while True:
                search_gray_window(found)
                r, g, b = pyautogui.pixel(2213, 211)
                print(f"Текущий цвет: {r}, {g}, {b}")

                if await is_green(r, g, b):
                    print("Цвет стал целевым!")
                    break

                if time.time() > end_time:
                    keyboard_press_key("e", 1)
                    end_time = time.time() + 30

            time.sleep(8)
            click(1508, 88, 5, 1)
            keyboard_press_key(Key.right, 2)
            keyboard_press_key(Key.down, 3)
            keyboard_press_key("enter", 1)
            time.sleep(5)
            keyboard_press_key("enter", 3)#сюжетный режим предпологаемый

        elif customer.order_des["version"].lower() == "legacy":
            time.sleep(115)
            click(2417, 1395, 10, 0.2)#сюжетный режим предпологаемый
            time.sleep(40)

        # await cherax_cliker(message) начало кликера в игре

        await reading_logs(message)

    except Exception as e:
        print(f"Ошибка в gta_cliker: {e}")
        print(traceback.format_exc())
        await error_handler(message.chat.id, traceback.format_exc())


# async def cherax_cliker(message):
#     """Cherax Clicker - работа с меню"""
#     try:
#         chat_id = message.chat.id
#         customer = common.get_customer(chat_id)
#
#         keyboard_press_key('k', 1, 3)
#         keyboard_press_key('y', 1, 10)
#         click(1278, 779, 1, 3)
#         keyboard_press_key('o')
#
#         print("Загрузка в сессию")
#
#         if customer.order_des["version"].lower() == "enhanced":
#             time.sleep(10)
#         elif customer.order_des["version"].lower() == "legacy":
#             time.sleep(100)
#
#         keyboard_press_key('n', 1, 3)
#
#         # Обработка денег
#         if customer.order_des["amount"] is not None:
#             if customer.order_des["amount"].isdigit():
#                 click(x=527, y=162, times=2, t=2)
#                 click(x=418, y=351, times=2, t=2)
#                 click(x=408, y=164, times=2, t=2)
#                 click(x=496, y=189, times=2, t=2)
#
#                 nightclub = False
#                 time.sleep(5)
#                 r, g, b = pyautogui.pixel(120, 570)
#
#                 if r == 70 and g == 0 and 120 <= b <= 121:
#                     print("Nightclub есть")
#                     nightclub = True
#                     click(x=220, y=570, times=2, t=0.5)
#
#                 if nightclub:
#                     await night_club(message)
#                 else:
#                     click(141, 238, 2, 3)
#                     keyboard_press_key(Key.end, 1, 1)
#                     keyboard_press_key(Key.up, 1, 1)
#                     keyboard_press_key(Key.down, 1, 1)
#                     keyboard_press_key('enter', 1, 1)
#
#                     # Серия кликов
#                     click32(1376, 792, 10, 0.2)
#                     time.sleep(1)
#                     click32(1488, 1194, 10, 0.2)
#                     time.sleep(1)
#                     click32(1801, 401, 10, 0.2)
#                     time.sleep(1)
#                     click32(1604, 1360, 10, 0.2)
#                     time.sleep(1)
#                     click32(976, 1144, 10, 0.2)
#                     time.sleep(1)
#                     click32(964, 1316, 10, 0.2)
#                     time.sleep(1)
#                     click32(2079, 1310, 10, 0.2)
#                     time.sleep(5)
#                     click32(2101, 144, 10, 0.2)
#                     keyboard_press_key(Key.end)
#
#                     await night_club(message)
#
#         # Обработка уровней
#         if customer.order_des["levels"] is not None:
#             if customer.order_des["levels"].isdigit():
#                 click(81, 357, 2)
#                 click(136, 175)
#                 write_text(customer.order_des["levels"])
#                 click(140, 197, 2)
#
#         # Обработка unlocks
#         if customer.order_des["unlocks"] is not None:
#             if customer.order_des["unlocks"].lower() == "standard unlocks":
#                 keyboard_press_key('u', 1, 5)
#                 time.sleep(1)
#                 keyboard_press_key('o', 1, 15)
#                 keyboard_press_key('enter', 2)
#                 time.sleep(70)
#                 keyboard_press_key('n', 1, 1)
#                 keyboard_press_key('x', 1, 1)
#                 keyboard_press_key('i', 1, 1)
#                 keyboard_press_key('l', 1, 3)
#                 keyboard_press_key('z', 1, 1)
#
#         await send_screen(message)
#     except Exception as e:
#         print(f"Ошибка в cherax_cliker: {e}")
#         print(traceback.format_exc())
#         await error_handler(message.chat.id, traceback.format_exc())

# async def night_club(message):
#     """Обработка nightclub"""
#     try:
#         customer = common.get_customer(message.chat.id)
#
#         click(181, 371, 1)
#         write_text(customer.order_des["amount"])
#         click(125, 574)
#         time.sleep(1)
#         ctypes.windll.user32.ShowCursor(False)
#         click(220, 570)
#         time.sleep(1)
#
#         while True:
#             r, g, b = pyautogui.pixel(120, 570)
#             print(f"Текущий цвет: {r}, {g}, {b}")
#             if r == 70 and g == 0 and 120 <= b <= 121:
#                 print("Цвет стал целевым!")
#                 ctypes.windll.user32.ShowCursor(True)
#                 break
#             time.sleep(1)
#     except Exception as e:
#         print(f"Ошибка в night_club: {e}")

async def reading_logs(message):
    try:
        file_path = r"C:\Users\%USERNAME%\Documents\Cherax\Lua\GTA5SERVICE\Boosting\Logs.json"
        expanded_path = os.path.expandvars(file_path)

        # Ждем, пока файл появится
        while not os.path.exists(expanded_path):
            print("Ожидаем создания файла Logs.json")
            time.sleep(5)

        # Ждем Online == True
        check_online()

        keyboard_press_key('-', 1, 1)

        # Ждем Boosting_Completed == True
        while True:
            with open(expanded_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if data["Boosting_Completed"] == True:
                print("Boosting_Completed == True")
                break

            print("Ожидаем Boosting_Completed == True")
            time.sleep(5)
        time.sleep(5)

        keyboard_press_key('o', 1, 5)

        check_online()
        time.sleep(3)

        keyboard_press_key('z', 1, 1)

        await send_screen(message)

    except Exception as e:
        print(f"Ошибка в reading_logs: {e}")
        print(traceback.format_exc())
        await error_handler(message.chat.id, traceback.format_exc())


async def send_screen(message):
    """Отправка скриншота в Telegram"""
    try:
        chat_id = message.chat.id
        customer = common.get_customer(chat_id)

        # Делаем скриншот
        screenshot = pyautogui.screenshot()
        screenshot_path = r"D:\Repos\gta_screen.png"
        screenshot.save(screenshot_path)

        # Отправляем в телеграм
        with open(screenshot_path, 'rb') as photo:
            await bot.send_photo(chat_id, photo, caption="✅ Работа выполнена!")

        # Закрываем приложения
        if customer.clicker:
            await customer.clicker.close_apps(message)
    except Exception as e:
        print(f"Ошибка в send_screen: {e}")
        print(traceback.format_exc())
        await error_handler(message.chat.id, traceback.format_exc())

def check_online():
    while True:
        with open(expanded_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if data["Online"] == True:
            print("Online == True")
            break

        print("Ожидаем Online == True")
        time.sleep(5)