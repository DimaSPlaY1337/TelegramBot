import os
import time

from pygetwindow import PyGetWindowException

from src.Clikers.Digiseller.input_utils import *
import pyautogui
from pynput.keyboard import KeyCode
from src.Handlers.Digiseller.IO_utils import send_screenshot, set_numlock_state


async def c_cliker(token, dialog_id, message_text, customer):
    os.startfile(r"C:\Users\gamePC\Desktop\CheraxLoader.exe", 'runas')
    win = await wait_for_open("Cherax Loader", 5) or await find_window_by_size(900, 600, timeout=100)

    if win:
        win_top = win.top
        win_left = win.left

        time.sleep(3)
        click(x=win_left + 127, y=win_top + 175)
        if customer.order_des["version"] == "enhanced":
            click(x=win_left + 83, y=win_top + 207)

            click(x=win_left + 94, y=win_top + 207)
            if customer.platform == "steam":
                click(x=win_left + 96, y=win_top + 239)
            elif customer.platform == "rockstar":
                click(x=win_left + 72, y=win_top + 263, times=1, t=3)
        elif customer.order_des["version"] == "legacy":
            click(x=win_left + 117, y=win_top + 222)

            click(x=win_left + 94, y=win_top + 207)
            if customer.platform == "steam":
                click(x=win_left + 99, y=win_top + 246)
            elif customer.platform == "rockstar":
                click(x=win_left + 50, y=win_top + 305, times=1, t = 3)

        click(x=win_left + 91, y=win_top + 265, times=3, t = 0.2)

        await customer.clicker.rockstar_search(token, dialog_id, message_text, customer, 10, True)

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
                raise e  # Другие ошибки пробрасываем дальше

        #запускается игра
        win_rock.minimize()
        time.sleep(10)
        await gta_cliker(token, dialog_id, message_text, customer)

async def gta_cliker(token, dialog_id, message_text, customer):
    win_cherax = await wait_for_open("Cherax Loader", 5) or await find_window_by_size(900, 600, timeout=100)
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

    time.sleep(2)
    while True:
        r, g, b = pyautogui.pixel(2213, 211)
        print(f"Текущий цвет: {r}, {g}, {b}")
        if await is_green(r, g, b):
            print("Цвет стал целевым!")
            break

    time.sleep(8)
    click(1308,88, 5, 1)
    keyboard_press_key("e", 3)
    keyboard_press_key("enter", 1)

    time.sleep(5)
    keyboard_press_key("enter", 3)

    time.sleep(40)
    await cherax_cliker(token, dialog_id, message_text, customer)

async def cherax_cliker(token, dialog_id, message_text, customer):
    # Включаем NumLock перед использованием Numpad
    # set_numlock_state(0)  # 1 = включить, 0 = выключить
    # time.sleep(2)
    # keyboard_press_key(KeyCode.from_vk(0x61))#numpad 1

    keyboard_press_key('k', 1, 3)
    keyboard_press_key('y', 1, 10)
    click(1278, 779,1,3)
    keyboard_press_key('o')
    print("Загрузка в сессию")

    time.sleep(100)
    keyboard_press_key('n',1,3)
    if customer.order_des["amount"].isdigit():
        click(x=527, y=162, times=2, t=2)
        click(x=418, y=351, times=2, t=2)
        click(x=408, y=164, times=2, t=2)
        click(x=496, y=189, times=2, t=2)
        #121 412 and 172 426
        nightclub = False

        time.sleep(5)
        r, g, b = pyautogui.pixel(120, 570)
        if r == 70 and g == 0 and 120 <= b <= 121:
            print("Nightclub есть")
            nightclub = True

        if nightclub:
            await night_club(customer)
        else:
            click(141, 238,2, 3)
            # set_numlock_state(1)  # 1 = включить, 0 = выключить
            # time.sleep(1)
            keyboard_press_key(Key.end,1,1)#numpad 1
            keyboard_press_key(Key.up, 1, 1)
            keyboard_press_key(Key.down, 1, 1)
            keyboard_press_key('enter', 1, 1)
            click(1376,792,10, 0.2)
            time.sleep(1)
            click(1488, 1194,10, 0.2)
            time.sleep(1)
            click(1801, 401,10, 0.2)
            time.sleep(1)
            click(1604, 1360,10, 0.2)
            time.sleep(1)
            click(976, 1144,10, 0.2)
            time.sleep(1)
            click(964, 1316,10,0.2)
            time.sleep(1)
            click(2079, 1310,10, 0.2)
            time.sleep(5)
            click(2101, 144,10,0.2)
            keyboard_press_key(Key.end)
            await night_club(customer)

    if customer.order_des["levels"].isdigit():
        click(81,357,2)
        click(136,175)
        write_text(customer.order_des["levels"])
        click(140, 197,2)

    if customer.order_des["unlocks"] == "standard unlocks":
        keyboard_press_key('u', 1, 5)

    time.sleep(1)
    keyboard_press_key('o', 1, 15)
    keyboard_press_key('enter', 2)
    time.sleep(70)
    keyboard_press_key('n', 1, 1)
    keyboard_press_key('x', 1, 1)
    keyboard_press_key('i', 1, 1)
    keyboard_press_key('l', 1, 3)
    keyboard_press_key('z', 1, 1)
    # Скрин окна GTA:
    # screenshot = pyautogui.screenshot()
    # screenshot.save('gta_screen.png')
    await send_screen(token, dialog_id, message_text, customer)

async def night_club(customer):
    click(181, 371, 1)
    write_text(customer.order_des["amount"])
    click(125, 574)
    time.sleep(1)
    ctypes.windll.user32.ShowCursor(False)
    time.sleep(1)
    while True:
        r, g, b = pyautogui.pixel(120, 558)
        print(f"Текущий цвет: {r}, {g}, {b}")
        if r == 70 and g == 0 and 120 <= b <= 121:
            print("Цвет стал целевым!")
            ctypes.windll.user32.ShowCursor(True)
            break
    time.sleep(1)

async def send_screen(token, dialog_id, message_text, customer):
    await send_screenshot(token, dialog_id, message_text, r"D:\Repos\gta_screen.png")
    await customer.clicker.close_apps(token, dialog_id, message_text, customer)

# click(x=492, y=178, times=1, t=2)
#
#     #крутим деньги
#     if customer.order_des["amount"].isdigit():
#         r, g, b = pyautogui.pixel(161, 411)
#         order = int(customer.order_des["amount"])
#         if r == g == b == 255:
#             click(x=492, y=178, times=1, t=1)
#             pyautogui.hotkey('ctrl', 'a')
#             time.sleep(1)
#             write_text(order)
#             time.sleep(1)
#             click(x=120, y=571, times=1, t=3)#start
#             ctypes.windll.user32.ShowCursor(False)
#
#             #проверка снятия start
#             while True:
#                 r, g, b = pyautogui.pixel(161, 411)
#                 print(f"Текущий цвет: {r}, {g}, {b}")
#                 if r==70 and g==0 and b==121:
#                     print("Цвет стал целевым!")
#                     ctypes.windll.user32.ShowCursor(True)
#                     break
#
#     time.sleep(1)
#     #крутим уровень
#     if customer.order_des["levels"].isdigit():
#         order = int(customer.order_des["levels"])
#         click(x=88, y=344)
#
#         click(x=130, y=167)
#         pyautogui.hotkey('ctrl', 'a')
#         time.sleep(1)
#         write_text(order)
#         time.sleep(1)
#         click(x=133, y=192)
#         keyboard_press_key('y')#смена сессии
#
#         while True:
#             r, g, b = pyautogui.pixel(1368, 620)
#             print(f"Текущий цвет: {r}, {g}, {b}")
#             if r == 240 and g == 201 and b == 80:
#                 print("Цвет стал целевым!")
#                 break
#
#         keyboard_press_key('enter', 1, 8)
#
#     time.sleep(1)
#     click(77, 356)
#     if customer.order_des["unlocks"] == "Standard Unlocks":
#         print("Делаем unlocks")
#     elif customer.order_des["unlocks"] == "Super Unlocks":
#         print("Делаем unlocks")