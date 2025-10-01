import ctypes
import os
import time
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

        time.sleep(10)
        click(x=win_left + 127, y=win_top + 175)
        if globals.order_des[message.chat.id]["version"] == "Enhanced":
            click(x=win_left + 83, y=win_top + 207)

            click(x=win_left + 94, y=win_top + 207)
            if globals.platform == "Steam":
                click(x=win_left + 96, y=win_top + 239)
            elif globals.platform == "Rockstar":
                click(x=win_left + 108, y=win_top + 267, times=1, t=3)
        elif globals.order_des[message.chat.id]["version"] == "Legacy":
            click(x=win_left + 117, y=win_top + 222)

            click(x=win_left + 94, y=win_top + 207)
            if globals.platform == "Steam":
                click(x=win_left + 106, y=win_top + 238)
            elif globals.platform == "Rockstar":
                click(x=win_left + 110, y=win_top + 303, times=1, t = 3)

        click(x=win_left + 91, y=win_top + 265, times=3, t = 0.2)

        await rockstar_search(message)

        win_rock = await wait_for_open("Rockstar Games Launcher", 100)
        if win_rock:
            win_left = win_rock.left
            win_top = win_rock.top

            win.resizeTo(1024, 600)
            time.sleep(1)
            win.activate()
            time.sleep(5)
            click(x=win_left + 905, y=win_top + 395, times=1, t = 3)

        #запускается игра
        time.sleep(10)
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

async def is_green(r, g, b, min_g=150, max_g=160, diff_rg=30, diff_bg=10):
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

def click(x, y, times=1, t=2):
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

@bot.message_handler(func=lambda m: globals.user_step.get(m.chat.id, {}).get("step") == "rock_c_guard")
async def rockstar_cliker(message):
    global win_left, win_top, sign_in_rock_button

    rock_guard = message.text
    print(f"Получили rock guard: {rock_guard}")
    await bot.send_message(message.chat.id, "Спасибо! Код получен.")

    pyautogui.click(x=win_left + 233, y=win_top + 475)
    time.sleep(0.2)
    pyautogui.write(rock_guard, interval=0.05)
    pyautogui.click(x=win_left + 527, y=sign_in_rock_button)

    time.sleep(6)
    if await is_error(368, 508, 388, 511):  # узнать коор ошибки при вводе кода
        await bot.send_message(message.chat.id, "Код введен неверно, введите еще раз.")
        sign_in_rock_button = win_top + 622

async def rockstar_search(message):
    global win_left, win_top, sign_in_rock_button

    win_rock = await wait_for_open("Rockstar Games - Sign In", 100)
    if win_rock:
        win_left = win_rock.left
        win_top = win_rock.top
        sign_in_rock_button = win_top + 601

        globals.user_step[message.chat.id] = {"step": "rock_c_guard"}
        await bot.send_message(message.chat.id, "Введите код RockStar Guard (или другой нужный код):")

async def is_error(x1, y1, x2, y2):
    global win_left, win_top
    rc,  rg, rb = 0, 0, 0
    for x in range(x1, x2):
        for y in range(y1, y2):
            r, g, b = pyautogui.pixel(win_left + x, win_top + y)
            # print(f"Цвет возможной ошибки: {r}, {g}, {b}")
            if await is_red(r, g, b):
                print("Здесь введен неверный пароль или логин")
                return True
    return False

async def is_red(r, g, b, r_min=80, diff_g=40, diff_b=40):
    # Проверка: ярко-красный или просто любой "красный"
    return (r > r_min) and (r - g > diff_g) and (r - b > diff_b)