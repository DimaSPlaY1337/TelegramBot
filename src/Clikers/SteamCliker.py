import ctypes
import os
import subprocess
import time
import pyautogui
from pynput.keyboard import Controller, Key
import win32gui
import win32con
import win32api

from src.Handlers import globals
import pygetwindow as gw

from src.Handlers.ChoosingPlatform import change_pass_and_login
from src.common import bot

win_left = None
win_top = None

guard_rock_x = None
guard_rock_y = None

guard_enter_rock_x = None
guard_enter_rock_y = None

gta = None

@bot.message_handler(func=lambda m: globals.user_step.get(m.chat.id, {}).get("step") == "steam_guard")
async def handle_steam_guard(message):
    global win_left, win_top

    steam_guard = message.text  # Здесь — то, что ввел пользователь!
    print(f"Получили steam guard: {steam_guard}")

    # globals.user_step[message.chat.id] = {"step": "complete"}  # или другой шаг, если надо
    win = await wait_for_steam_open("Sign in to Steam", 5) or None
    if win:
        await bot.send_message(message.chat.id, "Спасибо! Код получен.")

        win_top = win.top
        win_left = win.left

        pyautogui.click(x=win_left + 469, y=win_top + 185)
        pyautogui.write(steam_guard, interval=0.05)
        pyautogui.press('enter')

        time.sleep(2)
        if not await is_error(266, 151, 293, 161):#узнать коор ошибки при вводе кода
            await rockstar_search(message)
        else:
            await bot.send_message(message.chat.id, "Код введен неверно, введите еще раз.")
            pyautogui.click(x=win_left + 469, y=win_top + 185)
            pyautogui.press('backspace', 5)
    else:
        await rockstar_search(message)
        print("Окно steam guard не найдено")


async def wait_for_steam_open(title="Steam", timeout=30, interval=1):
    """
    Ждёт появления окна Steam с заголовком, максимум timeout секунд.
    Возвращает True, если окно найдено, иначе False
    """
    end_time = time.time() + timeout
    while time.time() < end_time:
        windows = gw.getWindowsWithTitle(title)
        exact_windows = [w for w in windows if w.title == title]
        if exact_windows:
            print(f"Окно {title} открыто!")
            return exact_windows[0]
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

    os.startfile("C:\\Program Files\\Rockstar Games\\Launcher\\LauncherPatcher.exe")

    # windows = gw.getAllWindows()
    # print([w.title for w in windows])

    time.sleep(7)

    win_be = None
    if not await wait_for_steam_open("C:\\Users\\gamePC\\Desktop\\beSkip.exe", 3):
        os.startfile(r"C:\Users\gamePC\Desktop\beSkip.exe", 'runas')
        win_be = await wait_for_steam_open("C:\\Users\\gamePC\\Desktop\\beSkip.exe")
    else:
        win_be = await wait_for_steam_open("C:\\Users\\gamePC\\Desktop\\beSkip.exe")

    # windows = gw.getAllWindows()
    # print([w.title for w in windows])

    os.startfile("C:\\Program Files (x86)\\Steam\\Steam.exe")
    switch_to_english()

    offset_plus_x = 445  # смещение по X от левого верхнего угла окна
    offset_plus_y = 220  # смещение по Y от левого верхнего угла окна

    offset_login_x = 145  # смещение по X от левого верхнего угла окна
    offset_login_y = 150  # смещение по Y от левого верхнего угла окна

    offset_password_x = offset_login_x  # смещение по X от левого верхнего угла окна
    offset_password_y = offset_plus_y  # смещение по Y от левого верхнего угла окна

    offset_enter_x = 325  # смещение по X от левого верхнего угла окна
    offset_enter_y = 300  # смещение по Y от левого верхнего угла окна

    time.sleep(0.5)
    win = await wait_for_steam_open("Sign in to Steam", 100) or await wait_for_steam_open("Войти в Steam", 100)
    if win:
        win.resizeTo(705, 440)
        time.sleep(0.2)
        win.activate()
        win_left = win.left
        win_top = win.top

        abs_x = win_left + offset_plus_x
        abs_y = win_top + offset_plus_y

        time.sleep(0.5)  # время на переключение окна
        pyautogui.click(x=abs_x, y=abs_y)
        # time.sleep(1)

        login_x = win_left + offset_login_x
        login_y = win.top + offset_login_y


        win.activate()
        time.sleep(0.2)
        pyautogui.click(x=login_x, y=login_y)
        pyautogui.click(x=login_x, y=login_y)
        write_data(login_x, login_y, globals.data_for_reg[message.chat.id]["login"])

        pass_x = win_left + offset_password_x
        pass_y = win.top + offset_password_y


        win.activate()
        time.sleep(0.2)
        pyautogui.click(x=pass_x, y=pass_y)
        pyautogui.click(x=pass_x, y=pass_y)
        write_data(pass_x, pass_y, globals.data_for_reg[message.chat.id]["password"])

        pass_cb_x = win_left + offset_enter_x
        pass_cb_y = win.top + offset_enter_y

        pyautogui.click(x=pass_cb_x, y=pass_cb_y)

        add_kode_x = win_left + 352
        add_kode_y = win_top + 320

        pyautogui.click(x=add_kode_x, y=add_kode_y)

        if not await is_error(51, 339, 121, 352):
            globals.user_step[message.chat.id] = {"step": "steam_guard"}
            await bot.send_message(message.chat.id, "Введите код Steam Guard (или другой нужный код):")
        else:
            win.close()
            await change_pass_and_login(message)
    else:
        print("Окно не найдено")

@bot.message_handler(func=lambda m: globals.user_step.get(m.chat.id, {}).get("step") == "rock_steam_guard")
async def rockstar_cliker(message):
    rock_guard = message.text
    print(f"Получили rock guard: {rock_guard}")
    await bot.send_message(message.chat.id, "Спасибо! Код получен.")

    win_left = globals.rock_win.left
    win_top = globals.rock_win.top

    r, g, b = pyautogui.pixel(2450, 1107)

    pyautogui.click(x=win_left + 233, y=win_top + 485)
    time.sleep(0.2)
    pyautogui.write(rock_guard, interval=0.05)
    pyautogui.click(x=win_left + 527, y=win_top + 601)

    if await is_error(430, 650, 440, 660):  # узнать коор ошибки при вводе кода
        await bot.send_message(message.chat.id, "Код введен неверно, введите еще раз.")
    else:
        await rockstar_acceptance(message, r, g, b)

async def rockstar_search(message):
    win_rock = await wait_for_steam_open("Rockstar Games - Sign In", 100)
    if win_rock:
        globals.rock_win = win_rock
        globals.user_step[message.chat.id] = {"step": "rock_steam_guard"}
        await bot.send_message(message.chat.id, "Введите код RockStar Guard (или другой нужный код):")
        globals.app_list.append(win_rock)
    else:
        await launch_prog(message)

async def rockstar_acceptance(message, r ,g ,b):
    time.sleep(3)
    pyautogui.click(x=2450, y=1107)#узнать координаты
    time.sleep(3)
    await launch_prog(message)

    # r_after, g_after, b_after = pyautogui.pixel(2450, 1107)
    # diff_r = abs(r_after - r)
    # diff_g = abs(g_after - g)
    # diff_b = abs(b_after - b)
    # if diff_b == diff_g == diff_r == 15: #узнать offset
    #     pyautogui.click(x=win_left + 233, y=win_top + 485)
    #     time.sleep(5)
    #     await launch_prog(message)
    # else:
    #     print("Подтверждение rockstar не появилось")

def is_blackout(r, g, b, diff=15):
    return abs(r - g) <= diff and abs(r - b) <= diff and abs(g - b) <= diff

async def launch_prog(message):
    global gta
    if globals.order_des[message.chat.id]["version"] == "Enhanced":
        # os.startfile(r"C:\Users\gamePC\Desktop\GTA`s\GTA_SE.url")
        os.startfile("steam://run/3240220")
        # subprocess.Popen(["C:\\Program Files (x86)\\Steam\\Steam.exe", "-applaunch", "3240220"])
    elif globals.order_des[message.chat.id]["version"] == "Legacy":
        # os.startfile(r"C:\Users\gamePC\Desktop\GTA`s\GTA_SL.url")
        os.startfile("steam://run/271590")
        # subprocess.Popen(["C:\\Program Files (x86)\\Steam\\Steam.exe", "-applaunch", "271590"])
    else:
        print("Ошибка выбора версии GTA")

    win_gta = await wait_for_steam_open("Grand Theft Auto V", 200)
    gta = win_gta

    if globals.order_des[message.chat.id]["version"] == "Enhanced":
        os.startfile(r"C:\Users\gamePC\Desktop\Enhanced.exe")
    elif globals.order_des[message.chat.id]["version"] == "Legacy":
        os.startfile(r"C:\Users\gamePC\Desktop\Legacy.exe")
    else:
        print("Ошибка выбора версии Sunrise")

    win_sun = await wait_for_steam_open("Sunrise", 100)
    # globals.app_list.append(win_sun)

    found = False
    time.sleep(10)
    if win_gta and win_sun:
        end_time = time.time() + 90
        while time.time() < end_time:
            r,g,b = pyautogui.pixel(2183, 1097)
            if is_gray(r,g,b) and found == False:
                keyboard_press_key('enter')
                found = True
            win_gta.activate()
            win_sun.minimize()
            time.sleep(2.5)
        from src.Clikers.GTACliker import gta_cliker
        await gta_cliker(message)

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

def is_gray(r, g, b, diff=15, min_val=50, max_val=230):
    # Серый: все каналы примерно равны, а значение не экстремальное
    return (
        abs(r - g) <= diff and abs(r - b) <= diff and abs(g - b) <= diff and
        min_val < r < max_val and min_val < g < max_val and min_val < b < max_val
    )

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

async def steam_exit():
    global win_left, win_top

    offset_profile_x = 200  # смещение по X от левого верхнего угла окна
    offset_profile_y = 13  # смещение по Y от левого верхнего угла окна

    offset_out_x = 944  # смещение по X от левого верхнего угла окна
    offset_out_y = 209  # смещение по Y от левого верхнего угла окна

    win = await wait_for_steam_open("Steam")
    time.sleep(1)
    win.activate()
    if win:
        win_right = win.right
        win_top = win.top

        abs_x = win_right - offset_profile_x
        abs_y = win_top + offset_profile_y

        time.sleep(0.5)  # время на переключение окна
        pyautogui.click(x=abs_x, y=abs_y)

        login_x = abs_x
        login_y = win.top + offset_out_y

        pyautogui.click(x=login_x, y=login_y)

        center_x = win.left + win.width // 2 + 100
        center_y = win.top + win.height // 2 + 75

        time.sleep(0.5)
        pyautogui.click(x=center_x, y=center_y)

        win.close()
    else:
        print("Окно не найдено")

async def close_apps():
    # выход из гта
    pyautogui.hotkey('alt', 'f4')
    if gta is not None:
        gta.activate()
    time.sleep(7)
    keyboard_press_key('enter')
    print("Вышли из GTA")

    time.sleep(5)

    win_rock = await wait_for_steam_open("Rockstar Games Launcher", 20) or None
    if win_rock is not None:
        win_rock.close()

    for win in globals.app_list:
        print("Закрываем")
        if win is not None:
            win.close()
        else:
            print("При закрытие окна, оно оказалось None")

    print("Закрываем Steam1")
    await steam_exit()

    print("Закрываем Steam2")
    win = await wait_for_steam_open("Sign in to Steam", 100) or await wait_for_steam_open("Войти в Steam", 100)
    if win:
        win.close()

    time.sleep(1)

    await close_sunrise()

async def close_sunrise():
    win = await wait_for_steam_open("Sunrise", 40)
    time.sleep(1)
    win.activate()
    if win:
        # win.resizeTo(755, 525)
        time.sleep(0.3)
        win_right = win.left
        win_top = win.top

        abs_x = win_right + 742
        abs_y = win_top + 13

        time.sleep(0.3)  # время на переключение окна
        lowlevel_click(abs_x, abs_y)
        print("rjytw")

    else:
        print("Окно не найдено")

def lowlevel_click(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)
    time.sleep(0.01)
    ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTDOWN
    time.sleep(0.01)
    ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTUP

def post_message_click(hwnd, x, y):
    lParam = win32api.MAKELONG(x, y)
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)