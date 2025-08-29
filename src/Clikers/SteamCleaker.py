import ctypes
import os
import time
import pyautogui
from src.Handlers import globals
import pygetwindow as gw

from src.Handlers.ChoosingPlatform import change_pass_and_login
from src.common import bot

win_left = None
win_top = None

guard_x = None
guard_y = None

guard_rock_x = None
guard_rock_y = None

guard_enter_rock_x = None
guard_enter_rock_y = None

rock_win = None

@bot.message_handler(func=lambda m: globals.user_step.get(m.chat.id, {}).get("step") == "steam_guard")
async def handle_steam_guard(message):
    steam_guard = message.text  # Здесь — то, что ввел пользователь!
    print(f"Получили steam guard: {steam_guard}")
    # Здесь можно:
    # — записать steam_guard куда надо
    # — изменить шаг состояния, чтобы не ловить дальше любые сообщения
    # — продолжить логику (например, отправить steam_guard дальше или завершить процесс)
    globals.user_step[message.chat.id] = {"step": "complete"}  # или другой шаг, если надо
    await bot.send_message(message.chat.id, "Спасибо! Код получен.")
    pyautogui.click(x=guard_x, y=guard_y)
    pyautogui.write(steam_guard, interval=0.05)
    pyautogui.press('enter')
    await gta_cliker(message)

async def wait_for_steam_open(title="Steam", timeout=30, interval=1):
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

def write_data(x, y,  data):
    pyautogui.click(x=x, y=y)
    pyautogui.click(x=x, y=y)
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.3)
    pyautogui.write(data, interval=0.05)

@bot.message_handler(func=lambda m: globals.user_step.get(m.chat.id, {}).get("step") == "cliker_steam")
async def steam_cliker(message):
    global win_left, win_top
    os.startfile("C:\\Program Files (x86)\\Steam\\Steam.exe")
    switch_to_english()
    global guard_x, guard_y

    offset_plus_x = 445  # смещение по X от левого верхнего угла окна
    offset_plus_y = 220  # смещение по Y от левого верхнего угла окна

    offset_login_x = 145  # смещение по X от левого верхнего угла окна
    offset_login_y = 150  # смещение по Y от левого верхнего угла окна

    offset_password_x = offset_login_x  # смещение по X от левого верхнего угла окна
    offset_password_y = offset_plus_y  # смещение по Y от левого верхнего угла окна

    offset_enter_x = 325  # смещение по X от левого верхнего угла окна
    offset_enter_y = 300  # смещение по Y от левого верхнего угла окна

    # windows = gw.getAllWindows()
    # print([w.title for w in windows])
    time.sleep(0.5)
    win = await wait_for_steam_open("Войти в Steam")
    if win:
        win_left = win.left
        win_top = win.top

        abs_x = win_left + offset_plus_x
        abs_y = win_top + offset_plus_y

        time.sleep(0.5)  # время на переключение окна
        pyautogui.click(x=abs_x, y=abs_y)
        # time.sleep(1)

        login_x = win_left + offset_login_x
        login_y = win.top + offset_login_y

        guard_x = login_x+100
        guard_y = login_y+10

        pyautogui.click(x=login_x, y=login_y)
        pyautogui.click(x=login_x, y=login_y)
        write_data(login_x, login_y, globals.data_for_reg[message.chat.id]["login"])

        pass_x = win_left + offset_password_x
        pass_y = win.top + offset_password_y

        pyautogui.click(x=pass_x, y=pass_y)
        pyautogui.click(x=pass_x, y=pass_y)

        write_data(pass_x, pass_y, globals.data_for_reg[message.chat.id]["password"])

        pass_cb_x = win_left + offset_enter_x
        pass_cb_y = win.top + offset_enter_y

        pyautogui.click(x=pass_cb_x, y=pass_cb_y)

        add_kode_x = win_left + 352
        add_kode_y = win_top + 320

        pyautogui.click(x=add_kode_x, y=add_kode_y)
        if not await is_error():
            globals.user_step[message.chat.id] = {"step": "steam_guard"}
            await bot.send_message(message.chat.id, "Введите код Steam Guard (или другой нужный код):")
        else:
            win.close()
            await change_pass_and_login(message)
    else:
        print("Окно не найдено")

@bot.message_handler(func=lambda m: globals.user_step.get(m.chat.id, {}).get("step") == "rock_steam_guard")
async def handle_rockstar_guard(message):
    global guard_rock_x, guard_rock_y, guard_enter_rock_x, guard_enter_rock_y
    rock_guard = message.text  # Здесь — то, что ввел пользователь!
    print(f"Получили steam guard: {rock_guard}")
    await bot.send_message(message.chat.id, "Спасибо! Код получен.")

    guard_rock_x = rock_win.left + 318
    guard_rock_y = rock_win.top + 451

    guard_enter_rock_x = rock_win.left + 542
    guard_enter_rock_y = rock_win.top + 568

    pyautogui.click(x=guard_rock_x, y=guard_rock_y)
    pyautogui.write(rock_guard, interval=0.05)
    pyautogui.click(x=guard_enter_rock_x, y=guard_enter_rock_y)

async def gta_cliker(message):
    global rock_win
    os.startfile(r"C:\Users\gamePC\Desktop\GTA`s\GTA_ES.url")
    # win = await wait_for_steam_open("Grand Theft Auto V Enhanced")

    win = await wait_for_steam_open("Rockstar Games")
    if win:
        rock_win = win
        globals.user_step[message.chat.id] = {"step": "rock_steam_guard"}
        await bot.send_message(message.chat.id, "Введите код RockStar Guard (или другой нужный код):")

    os.startfile(r"C:\Users\gamePC\Desktop\Enhanced.exe")
    win = await wait_for_steam_open("Sunrise")

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
        pyautogui.keyUp('altleft')
        time.sleep(0.2)  # даём системе переключиться
        print("Сменили раскладку на английскую!")

async def is_red(x, y, r_min=80, diff_g=40, diff_b=40):
    r, g, b = pyautogui.pixel(win_left + x, win_top + y)
    # Проверка: ярко-красный или просто любой "красный"
    return (r > r_min) and (r - g > diff_g) and (r - b > diff_b)

async def is_error():
    x1, y1 = 51, 339
    x2, y2 = 121, 352
    for x in range(x1, x2):
        for y in range(y1, y2):
            r, g, b = pyautogui.pixel(win_left + x, win_top + y)
            if await is_red(r, g, b):
                print("Здесь введен неверный пароль или логин")
                return True

    return False