import ctypes
import os
from datetime import time
import pygetwindow as gw
import pyautogui

from src.Handlers import globals
from pynput.keyboard import Controller, Key, KeyCode
from src.common import bot


async def c_cliker(message):
    global win_left, win_top
    os.startfile(r"C:\Users\gamePC\Desktop\CheraxLoader.exe", 'runas')
    win = await wait_for_open("Cherax Loader", 100)

    if win:
        win_top = win.top
        win_left = win.left

        win.resizeTo(900, 600)
        time.sleep(3)
        pyautogui.click(x=win_left + 127, y=win_top + 175)
        if globals.order_des[message.chat.id]["version"] == "Enhanced":
            pyautogui.click(x=win_left + 83, y=win_top + 207)
        elif globals.order_des[message.chat.id]["version"] == "Legacy":
            pyautogui.click(x=win_left + 117, y=win_top + 222)

        time.sleep(1)
        pyautogui.click(x=win_left + 94, y=win_top + 207)
        if globals.platform == "Steam":
            pyautogui.click(x=win_left + 96, y=win_top + 241)
        elif globals.platform == "Rockstar":
            pyautogui.click(x=win_left + 86, y=win_top + 267)

        time.sleep(3)
        pyautogui.click(x=win_left + 91, y=win_top + 265)

        win_rock = await wait_for_open("Rockstar Games - Sign In", 100)
        if win_rock:
            win_left = win_rock.left
            win_top = win_rock.top

            win.resizeTo(1024, 600)
            time.sleep(1)
            win.activate()
            time.sleep(5)
            pyautogui.click(x=win_left + 905, y=win_top + 395)

        #запускается игра
        time.sleep(3)
        await gta_cliker(message)

async def gta_cliker(message):
    win_cherax = await wait_for_open("Cherax Loader", 5)
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
    await cherax_cliker(message)

async def cherax_cliker(message):
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
    if globals.order_des[message.chat.id]["amount"].isdigit():
        r, g, b = pyautogui.pixel(161, 411)
        order = int(globals.order_des[message.chat.id]["amount"])
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
    if globals.order_des[message.chat.id]["levels"].isdigit():
        order = int(globals.order_des[message.chat.id]["levels"])
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
    if globals.order_des[message.chat.id]["unlocks"] == "Standard Unlocks":
        print("Делаем unlocks")
    elif globals.order_des[message.chat.id]["unlocks"] == "Super Unlocks":
        print("Делаем unlocks")

    time.sleep(1)
    keyboard_press_key('i', 1, 3)
    keyboard_press_key('o', 1, 3)
    keyboard_press_key('z', 1, 3)
    # Скрин окна GTA:
    screenshot = pyautogui.screenshot()
    screenshot.save('gta_screen.png')
    time.sleep(1)
    await send_screenshot(message)

def is_green(r, g, b, min_g=150, max_g=160, diff_rg=30, diff_bg=10):
    """
    Находит зеленоватый цвет наподобие #889E98:
    - Зеленый больше других компонент.
    - Зеленый между min_g и max_g.
    - Разница Green-Red и Green-Blue не превышает diff_rg/diff_bg.
    """
    return (
        min_g <= g <= max_g and
        abs(g - r) <= diff_rg and
        abs(g - b) <= diff_bg and
        g > r and g > b
    )


async def wait_for_open(title="Steam", timeout=200, interval=1):
    """
    Ждёт появления окна Steam с заголовком, максимум timeout секунд.
    Возвращает True, если окно найдено, иначе False
    """
    end_time = time.time() + timeout
    while time.time() < end_time:
        windows = gw.getWindowsWithTitle(title)
        if windows:
            print(f"Окно {title} открыто!")
            return windows[0]
        print(f"Жду открытия окна {title}...")
        time.sleep(interval)
    print("Окно не появилось за отведённое время.")
    return None

def keyboard_press_key(key, times=1, interval=0.5):
    keyboard = Controller()
    if key == 'enter':
        key_to_press = Key.enter
    else:
        key_to_press = key
    for _ in range(times):
        keyboard.press(key_to_press)
        keyboard.release(key_to_press)
        time.sleep(interval)

def click(x, y, times=1, t: float = 2):
    for _ in range(times):
        pyautogui.click(x,y)
        time.sleep(t) # небольшая пауза между нажатиями 0.2

def write_text(text, interval=0.2):
    keyboard = Controller()
    for char in str(text):
        keyboard.press(char)
        keyboard.release(char)
        time.sleep(interval)

async def send_screenshot(message):
    with open(r'D:\Repos\gta_screen.png', 'rb') as photo:
        await bot.send_photo(message.chat.id, photo)
    # globals.platform = "Rockstar"
    await close_apps()

async def close_apps():
    from src.Clikers import EpicgamesCliker, RockstarCliker, SteamCliker
    if globals.platform == "EpicGames":
        await EpicgamesCliker.close_apps()
    elif globals.platform == "Rockstar":
        await RockstarCliker.close_apps()
    elif globals.platform == "Steam":
        await SteamCliker.close_apps()