import asyncio
import ctypes
import time
import win32api
import win32con
import pygetwindow as gw
import pyautogui
from pynput.keyboard import Controller, Key

def write_text(text, interval=0.2):
    keyboard = Controller()
    for char in str(text):
        keyboard.press(char)
        keyboard.release(char)
        time.sleep(interval)


    # windows = gw.getAllWindows()
    # print([w.title for w in windows])

# def write_data(x, y,  data):
#     pyautogui.click(x=x, y=y)
#     pyautogui.click(x=x, y=y)
#     time.sleep(0.5)
#     pyautogui.hotkey('ctrl', 'a')
#     time.sleep(0.3)
#     pyautogui.write(data, interval=0.05)

def write_data(x, y,  data):
    pyautogui.click(x=x, y=y)
    # time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.3)
    pyautogui.write(data, interval=0.05)

async def is_error(customer,x1, y1, x2, y2):
    for x in range(x1, x2):
        for y in range(y1, y2):
            r, g, b = pyautogui.pixel(customer.clicker.win_left + x, customer.clicker.win_top + y)
            print(f"Цвет возможной ошибки: {r}, {g}, {b}")
            if customer.platform == "Rockstar":
                if r==189 and g==8 and b==8:
                    print("Здесь введен неверный пароль или логин")
                    return True
            elif await is_red(r, g, b):
                    print("Здесь введен неверный пароль или логин")
                    return True
    return False

# async def is_red(r, g, b, r_min=80, diff_g=40, diff_b=40):
#     # Проверка: ярко-красный или просто любой "красный"
#     return r==189 and g==8 and b==8

async def is_red(r, g, b, r_min=80, diff_g=40, diff_b=40):
    # Проверка: ярко-красный или просто любой "красный"
    return (r > r_min) and (r - g > diff_g) and (r - b > diff_b)

async def is_green(r, g, b, min_g=119, max_g=160, diff_rg=30, diff_bg=15):
    """
    Находит зеленоватый цвет наподобие #889E98:
    - Зеленый больше других компонент.
    - Зеленый между min_g и max_g.
    - Разница Green-Red и Green-Blue не превышает diff_rg/diff_bg.
    """
    b1 = (
        min_g <= g <= max_g and
        abs(g - r) <= diff_rg and
        abs(g - b) <= diff_bg and
        g > r and g > b
    )
    # b2 = r == 97 and g == 120 and b == 108
    # r1, g1, bb = pyautogui.pixel(374, 99)
    # b3 = r1 == g1 == bb == 202
    # b4 = r == 115 and g == 143 and b == 128
    return b1

# async def is_gray(r, g, b, diff=11):
#     """
#     Проверяет, является ли цвет (r, g, b) серым.
#     Аргумент diff — допустимый максимальный допуск между компонентами.
#     Для идеального серого все компоненты равны, но на практике допускается небольшое отклонение.
#     """
#     print(f" Цвет поля: {r}, {g}, {b}")
#     return abs(r - g) <= diff and abs(r - b) <= diff and abs(g - b) <= diff

def search_gray_window(found):
    r, g, b = pyautogui.pixel(840, 1075)
    if is_gray(r, g, b) and found == False:
        click(2369, 148)
        keyboard_press_key('enter')
        print("Нашли серое окно GTA")
        found = True

def is_gray(r, g, b, diff=3, min_val=26, max_val=159):
    """
    Проверяет, является ли цвет тёмно-серым: оттенки типа 1A1A1A, 1D1D1D и похожие.
    """
    return (
        abs(r - g) <= diff and
        abs(r - b) <= diff and
        abs(g - b) <= diff and
        min_val <= r <= max_val and
        min_val <= g <= max_val and
        min_val <= b <= max_val
    )

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


async def find_window_by_size(target_width, target_height, timeout=30, interval=1):
    """
    Ищет окно по размеру
    """
    deadline = time.time() + timeout

    while time.time() < deadline:
        for win in gw.getAllWindows():
            if win.width == target_width and win.height == target_height and win.visible:
                print(f"Найдено окно по размеру: {win.title}")
                return win
        await asyncio.sleep(interval)

    return None

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

def press_key(key, times=1):
    for _ in range(times):
        pyautogui.press(key)
        time.sleep(0.3) # небольшая пауза между нажатиями 0.2

def click32(x, y, times=1, t=1):
    for _ in range(times):
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        time.sleep(t)

def click(x, y, times=1, t=1):
    for _ in range(times):
        pyautogui.click(x,y)
        time.sleep(t) # небольшая пауза между нажатиями 0.2

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