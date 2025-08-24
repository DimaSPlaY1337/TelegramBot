import ctypes
import os
import time
import pyautogui
from src.Handlers import globals
import pygetwindow as gw
from src.common import bot

guard_x = None
guard_y = None

guard_enter_x = None
guard_enter_y = None

win_right = None
win_top = None

async def rockstar_client(message):
    global win_right, win_top
    win = await wait_for_rockstar_open("Rockstar Games")
    win_right = win.left
    win_top = win.top

    end_time = time.time() + 200
    while time.time() < end_time:
        if await check_pixel(message, 957, 51, 0xFF, 0xF8, 0xC9):
            print(f"Окно client открыто!")
            break
        print(f"Жду открытия окна client...")
        time.sleep(1)
    print("Окно client не появилось за отведённое время.")

    settings_button_r = win_right + 992
    settings_button_t = win_top + 64
    pyautogui.click(x=settings_button_r, y=settings_button_t)

    battle_eye_x = win_right + 1035
    battle_eye_y = win_top + 416
    if not await check_pixel(message, battle_eye_x, battle_eye_y, 0x13, 0x15, 0x18):
        pyautogui.click(x=battle_eye_x, y=battle_eye_y)

@bot.message_handler(func=lambda m: globals.user_step.get(m.chat.id, {}).get("step") == "rockstar_guard")
async def handle_rockstar_guard(message):
    steam_guard = message.text  # Здесь — то, что ввел пользователь!
    print(f"Получили steam guard: {steam_guard}")
    # Здесь можно:
    # — записать steam_guard куда надо
    # — изменить шаг состояния, чтобы не ловить дальше любые сообщения
    # — продолжить логику (например, отправить steam_guard дальше или завершить процесс)
    await bot.send_message(message.chat.id, "Спасибо! Код получен.")
    pyautogui.click(x=guard_x, y=guard_y)
    pyautogui.write(steam_guard, interval=0.05)
    pyautogui.click(x=guard_enter_x, y=guard_enter_y)

    await rockstar_client(message)

async def wait_for_rockstar_open(title="Steam", timeout=30, interval=1):
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

async def check_pixel(message, x, y, c_x, c_y, c_z):
    pixel_color1 = pyautogui.pixel(win_right + x, win_top + y)
    # Сравниваем с нужным цветом 0x05
    if pixel_color1 == (c_x, c_y, c_z):
        print("Точка совпадает с цветом ошибки!")
        return True
    return False

@bot.message_handler(func=lambda m: globals.user_step.get(m.chat.id, {}).get("step") == "cliker_rockstar")
async def rockstar_cliker(message):
    # C:\\Program Files\\Rockstar Games\\Launcher\\LauncherPatcher.exe
    os.startfile("C:\\Program Files\\Rockstar Games\\Launcher\\LauncherPatcher.exe")
    switch_to_english()
    global guard_x, guard_y, guard_enter_x, guard_enter_y, win_right, win_top

    offset_plus_x = 445  # смещение по X от левого верхнего угла окна
    offset_plus_y = 220  # смещение по Y от левого верхнего угла окна

    offset_login_x = 250  # смещение по X от левого верхнего угла окна
    offset_login_y = 350  # смещение по Y от левого верхнего угла окна

    offset_password_x = 250  # смещение по X от левого верхнего угла окна
    offset_password_y = 420  # смещение по Y от левого верхнего угла окна

    offset_enter_x = 520  # смещение по X от левого верхнего угла окна
    offset_enter_y = 520  # смещение по Y от левого верхнего угла окна

    win = await wait_for_rockstar_open("Rockstar Games - Sign In")
    if win:
        win_right = win.right
        win_top = win.top

        login_x = win.left + offset_login_x
        login_y = win.top + offset_login_y

        guard_x = win.left + 318
        guard_y = win.top + 451

        guard_enter_x = win.left + 542
        guard_enter_y = win.top + 568

        pyautogui.click(x=login_x, y=login_y)
        pyautogui.click(x=login_x, y=login_y)
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.3)
        pyautogui.write('gutierrezstephen1600@outlook.com', interval=0.05)

        pass_x = win.left + offset_password_x
        pass_y = win.top + offset_password_y
        # o13S_JfAwU
        pyautogui.click(x=pass_x, y=pass_y)
        pyautogui.click(x=pass_x, y=pass_y)
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.3)
        pyautogui.write('o13S_JfAwU',interval=0.05)

        abs_x = win.left + offset_enter_x
        abs_y = win.top + offset_enter_y

        pyautogui.click(x=abs_x, y=abs_y)
        if (not await check_pixel(message, 408, 249, 189, 8,8)
                and not await check_pixel(message, 366, 386, 189,8,8)):
            globals.user_step[message.chat.id] = {"step": "rockstar_guard"}
            await bot.send_message(message.chat.id, "Введите код RockStar Guard (или другой нужный код):")
        else:
            #TO DO
            await bot.send_message(message.chat.id, "Введите еще раз")
    else:
        print("Окно не найдено")

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