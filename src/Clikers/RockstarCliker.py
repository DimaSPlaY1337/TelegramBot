import ctypes
import os
import time
import pyautogui

from src.Handlers import globals
import pygetwindow as gw

from src.Handlers.ChoosingPlatform import change_pass_and_login
from src.common import bot

guard_x = None
guard_y = None

win_left = 0
win_top = 0

app_list = []

@bot.message_handler(func=lambda m: globals.user_step.get(m.chat.id, {}).get("step") == "rockstar_guard")
async def handle_rockstar_guard(message):
    steam_guard = message.text  # Здесь — то, что ввел пользователь!
    print(f"Получили steam guard: {steam_guard}")
    # Здесь можно:
    # — записать steam_guard куда надо
    # — изменить шаг состояния, чтобы не ловить дальше любые сообщения
    # — продолжить логику (например, отправить steam_guard дальше или завершить процесс)
    await bot.send_message(message.chat.id, "Спасибо! Код получен.")
    # pyautogui.click(x=guard_x, y=guard_y)
    # pyautogui.write(steam_guard, interval=0.05)
    # pyautogui.click(x=win_left + 538, y= win_top + 563)

    if not await is_error(430, 650, 440, 660):#узнать коор ошибки при вводе кода
        await launch_prog(message)
    else:
        await bot.send_message(message.chat.id, "Код введен неверно, введите еще раз.")

async def wait_for_rockstar_open(title="Steam", timeout=200, interval=1):
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

@bot.message_handler(func=lambda m: globals.user_step.get(m.chat.id, {}).get("step") == "cliker_rockstar")
async def rockstar_cliker(message):
    os.startfile("C:\\Program Files\\Rockstar Games\\Launcher\\LauncherPatcher.exe")
    switch_to_english()
    global guard_x, guard_y, win_left, win_top

    offset_login_x = 250  # смещение по X от левого верхнего угла окна
    offset_login_y = 350  # смещение по Y от левого верхнего угла окна

    offset_password_x = 250  # смещение по X от левого верхнего угла окна
    offset_password_y = 420  # смещение по Y от левого верхнего угла окна

    offset_enter_x = 520  # смещение по X от левого верхнего угла окна
    offset_enter_y = 520  # смещение по Y от левого верхнего угла окна

    win = await wait_for_rockstar_open("Rockstar Games - Sign In")
    if win:
        win.resizeTo(700, 800)
        time.sleep(0.3)
        win.activate()
        time.sleep(0.2)
        win_left = win.left
        win_top = win.top

        login_x = win.left + offset_login_x
        login_y = win.top + offset_login_y

        guard_x = win.left + 318
        guard_y = win.top + 451

        write_data(login_x, login_y, globals.data_for_reg[message.chat.id]["login"])

        pass_x = win.left + offset_password_x
        pass_y = win.top + offset_password_y

        write_data(pass_x, pass_y, globals.data_for_reg[message.chat.id]["password"])

        abs_x = win.left + offset_enter_x
        abs_y = win.top + offset_enter_y

        pyautogui.click(x=abs_x, y=abs_y)

        time.sleep(4)
        if (not await is_error(101,186, 141, 204)
                and not await is_error(123,351, 134, 359)):
            globals.user_step[message.chat.id] = {"step": "rockstar_guard"}
            await bot.send_message(message.chat.id, "Введите код RockStar Guard (или другой нужный код):")
        else:
            win.close()
            await change_pass_and_login(message)
            await bot.send_message(message.chat.id, "Введите еще раз")
    else:
        print("Окно не найдено")

def write_data(x, y,  data):
    pyautogui.click(x=x, y=y)
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.3)
    pyautogui.press('delete')
    time.sleep(0.2)
    pyautogui.write(data, interval=0.01)

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

async def is_red(r, g, b, r_min=80, diff_g=40, diff_b=40):
    # Проверка: ярко-красный или просто любой "красный"
    return (r > r_min) and (r - g > diff_g) and (r - b > diff_b)

async def is_error(x1, y1, x2, y2):
    global win_left, win_top
    rc,  rg, rb = 0, 0, 0
    for x in range(x1, x2):
        for y in range(y1, y2):
            r, g, b = pyautogui.pixel(win_left + x, win_top + y)
            print(f"Цвет возможной ошибки: {r}, {g}, {b}")
            if await is_red(r, g, b):
                print("Здесь введен неверный пароль или логин")
                return True
    return False

async def rock_exit():
    global win_left, win_top

    offset_profile_x = 1031  # смещение по X от левого верхнего угла окна
    offset_profile_y = 67  # смещение по Y от левого верхнего угла окна

    offset_out_x = 969  # смещение по X от левого верхнего угла окна
    offset_out_y = 336  # смещение по Y от левого верхнего угла окна

    # windows = gw.getAllWindows()
    # print([w.title for w in windows])
    win = await wait_for_rockstar_open("Rockstar Games Launcher")
    time.sleep(1)
    win.activate()
    time.sleep(1)
    if win:
        win.resizeTo(1084, 877)
        win_left = win.left
        win_top = win.top

        abs_x = win_left + offset_profile_x
        abs_y = win_top + offset_profile_y

        pyautogui.click(x=abs_x, y=abs_y)

        login_x = win_left + offset_out_x
        login_y = win_top + offset_out_y

        time.sleep(0.2)
        pyautogui.click(x=login_x, y=login_y)
    else:
        print("Окно не найдено")

async def close_apps():
    global app_list
    for win in app_list:
        win.close()
    await rock_exit()

    win = await wait_for_rockstar_open("Rockstar Games - Sign In")
    if win:
        win.close()

async def launch_prog(message):
    global app_list
    os.startfile(r"C:\Users\gamePC\Desktop\GTA`s\GTA_RE.lnk")
    win_gta = await wait_for_rockstar_open("Grand Theft Auto V Enhanced")
    app_list.append(win_gta)

    os.startfile(r"C:\Users\gamePC\Desktop\Enhanced.exe")
    win_sun = await wait_for_rockstar_open("Sunrise")
    app_list.append(win_sun)

    if win_gta and win_sun:
        time.sleep(100)
        from src.Clikers.GTACliker import gta_cliker
        await gta_cliker(message)