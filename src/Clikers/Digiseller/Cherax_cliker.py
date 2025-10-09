import os
from pygetwindow import PyGetWindowException

from src.Clikers.Digiseller.input_utils import *
import pyautogui
from pynput.keyboard import KeyCode
from src.Handlers.Digiseller.IO_utils import send_screenshot_message


async def c_cliker(token, dialog_id, message_text, customer):
    os.startfile(r"C:\Users\gamePC\Desktop\CheraxLoader.exe", 'runas')
    win = await wait_for_open("Cherax Loader", 7) or await find_window_by_size(900, 600, timeout=100)

    if win:
        win_top = win.top
        win_left = win.left

        time.sleep(5)
        click(x=win_left + 127, y=win_top + 175)
        if customer.order_des["version"] == "enhanced":
            click(x=win_left + 83, y=win_top + 207)

            click(x=win_left + 94, y=win_top + 207)
            if customer.platform == "steam":
                click(x=win_left + 96, y=win_top + 239)
            elif customer.platform == "rockstar":
                click(x=win_left + 108, y=win_top + 267, times=1, t=3)
        elif customer.order_des["version"] == "legacy":
            click(x=win_left + 117, y=win_top + 222)

            click(x=win_left + 94, y=win_top + 207)
            if customer.platform == "steam":
                click(x=win_left + 106, y=win_top + 238)
            elif customer.platform == "rockstar":
                click(x=win_left + 110, y=win_top + 303, times=1, t = 3)

        click(x=win_left + 91, y=win_top + 265, times=3, t = 0.2)

        await customer.clicker.rockstar_search(token, dialog_id, message_text, customer, 10, True)

        win_rock = await wait_for_open("Rockstar Games Launcher", 100)
        try:
            if win_rock:
                win_left = win_rock.left
                win_top = win_rock.top

                win.resizeTo(1024, 600)
                time.sleep(1)
                win.activate()
                time.sleep(5)
                click(x=win_left + 905, y=win_top + 395, times=1, t=3)
        except PyGetWindowException as e:
            if "Error code from Windows: 0" in str(e):
                print("Окно успешно активировано (ложная ошибка)")
                click(x=win_left + 905, y=win_top + 395, times=1, t=3)
            else:
                raise e  # Другие ошибки пробрасываем дальше

        #запускается игра
        time.sleep(10)
        await gta_cliker(token, dialog_id, message_text, customer)

async def gta_cliker(token, dialog_id, message_text, customer):
    win_cherax = await wait_for_open("Cherax Loader", 10) or await find_window_by_size(900, 600, timeout=100)
    if win_cherax:
        win_cherax.minimize()
        print("Скрыли cherax")

    while True:
        r, g, b = pyautogui.pixel(2362, 334)
        print(f"Текущий цвет: {r}, {g}, {b}")
        if not await is_green(r, g, b):
            print("Цвет стал целевым!")
            break

    time.sleep(2)
    click(511,95, 10, 0.2)

    time.sleep(2)
    keyboard_press_key("enter", 3)

    time.sleep(30)
    await cherax_cliker(token, dialog_id, message_text, customer)

async def cherax_cliker(token, dialog_id, message_text, customer):
    keyboard_press_key(KeyCode.from_vk(0x61))#numpad 1

    time.sleep(4)
    click(x=72, y=506)
    click(x=141, y=200)
    keyboard_press_key('u')
    print("Загрузка в сессию")

    time.sleep(25)
    keyboard_press_key('y')
    time.sleep(4)
    click(x=1304, y=776, times=1, t=3)
    click(x=510, y=151)
    click(x=414, y=340)
    click(x=407, y=149)
    click(x=492, y=178)

    #крутим деньги
    if customer.order_des["amount"].isdigit():
        r, g, b = pyautogui.pixel(161, 411)
        order = int(customer.order_des["amount"])
        if r == g == b == 255:
            click(x=492, y=178, times=1, t=1)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(1)
            write_text(order)
            time.sleep(1)
            click(x=120, y=571, times=1, t=3)#start
            ctypes.windll.user32.ShowCursor(False)

            #проверка снятия start
            while True:
                r, g, b = pyautogui.pixel(161, 411)
                print(f"Текущий цвет: {r}, {g}, {b}")
                if r == 46 and g == 00 and b == 78:
                    print("Цвет стал целевым!")
                    ctypes.windll.user32.ShowCursor(True)
                    break

    time.sleep(1)
    #крутим уровень
    if customer.order_des["levels"].isdigit():
        order = int(customer.order_des["levels"])
        click(x=88, y=344)

        click(x=130, y=167)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(1)
        write_text(order)
        time.sleep(1)
        click(x=133, y=192)
        keyboard_press_key('y')#смена сессии

        while True:
            r, g, b = pyautogui.pixel(1368, 620)
            print(f"Текущий цвет: {r}, {g}, {b}")
            if r == 240 and g == 201 and b == 80:
                print("Цвет стал целевым!")
                break

        keyboard_press_key('enter', 1, 8)

    time.sleep(1)
    click(77, 356)
    if customer.order_des["unlocks"] == "Standard Unlocks":
        print("Делаем unlocks")
    elif customer.order_des["unlocks"] == "Super Unlocks":
        print("Делаем unlocks")

    time.sleep(1)
    keyboard_press_key('i', 1, 3)
    keyboard_press_key('o', 1, 3)
    keyboard_press_key('z', 1, 3)
    # Скрин окна GTA:
    screenshot = pyautogui.screenshot()
    screenshot.save('gta_screen.png')
    time.sleep(1)
    await send_screenshot(token, dialog_id, message_text, customer)

async def send_screenshot(token, dialog_id, message_text, customer):
    await send_screenshot_message(token, dialog_id, message_text, r"D:\Repos\gta_screen.png")
    await customer.clicker.close_apps()