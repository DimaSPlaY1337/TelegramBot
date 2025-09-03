import ctypes
import pyautogui
import time
from pynput.keyboard import Controller, Key

from src.Clikers import EpicgamesCliker, RockstarCliker, SteamCliker
from src.Handlers import globals

from src.common import bot


def press_key(key, times=1):
    for _ in range(times):
        pyautogui.press(key)
        time.sleep(0.2) # небольшая пауза между нажатиями

def keyboard_press_key(key, times=1, interval=0.5):
    keyboard = Controller()
    for _ in range(times):
        keyboard.press(key)
        keyboard.release(key)
        time.sleep(interval)

def write_text(text, interval=0.2):
    keyboard = Controller()
    for char in str(text):
        keyboard.press(char)
        keyboard.release(char)
        time.sleep(interval)

async def gta_cliker(message):
    keyboard = Controller()
    # Последовательность команд (по сообщениям)
    # f5
    press_key('f5')

    # 4 down
    press_key('down', 4)

    # enter
    press_key('enter')

    # enter
    press_key('enter')

    # galka
    press_key('enter')

    # 1 down
    press_key('down', 1)
    press_key('enter')

    # write order
    sum = 100000000
    order = 75000000
    if sum > order:
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
    else:
        keyboard.type(str(order))
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        press_key('enter')

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
    order = 1000
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

    # down 1
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
    await send_screenshot(message)

async def is_gray(r, g, b, diff=11):
    """
    Проверяет, является ли цвет (r, g, b) серым.
    Аргумент diff — допустимый максимальный допуск между компонентами.
    Для идеального серого все компоненты равны, но на практике допускается небольшое отклонение.
    """
    print(f" Цвет поля: {r}, {g}, {b}")
    return abs(r - g) <= diff and abs(r - b) <= diff and abs(g - b) <= diff


async def is_red(r, g, b, r_min=80, diff_g=40, diff_b=40):
    # Проверка: ярко-красный или просто любой "красный"
    return (r > r_min) and (r - g > diff_g) and (r - b > diff_b)

def switch_to_english():
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    curr_window = user32.GetForegroundWindow()
    thread_id = user32.GetWindowThreadProcessId(curr_window, 0)
    klid = user32.GetKeyboardLayout(thread_id)
    lid = klid & (2**16 - 1)
    lid_hex = hex(lid)
    if lid_hex == '0x419':  # если русский
        pyautogui.keyDown('altleft')
        pyautogui.press('shiftleft')
        time.sleep(0.3)
        pyautogui.keyUp('altleft')
        time.sleep(0.3)  # даём системе переключиться
        print("Сменили раскладку на английскую!")


async def send_screenshot(message):
    with open(r'D:\Repos\gta_screen.png', 'rb') as photo:
        await bot.send_photo(message.chat.id, photo)
    await close_apps()

async def close_apps():
    if globals.platform == "EpicGames":
        await EpicgamesCliker.close_apps()
    elif globals.platform == "Rockstar":
        await RockstarCliker.close_apps()
    elif globals.platform == "Steam":
        await SteamCliker.close_apps()
