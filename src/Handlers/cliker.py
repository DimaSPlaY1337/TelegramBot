import os
import time
import pyautogui
from src.Handlers import globals
import pygetwindow as gw
from src.common import bot

guard_x = None
guard_y = None

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

async def wait_for_steam_open(title="Steam", timeout=30, interval=1):
    """
    Ждёт появления окна Steam с заголовком, максимум timeout секунд.
    Возвращает True, если окно найдено, иначе False
    """
    end_time = time.time() + timeout
    while time.time() < end_time:
        windows = gw.getWindowsWithTitle(title)
        if windows:
            print("Окно Steam открыто!")
            return windows[0]
        print("Жду открытия окна Steam...")
        time.sleep(interval)
    print("Окно не появилось за отведённое время.")
    return None

# await wait_for_steam_open("Steam", timeout=30)

@bot.message_handler(func=lambda m: globals.user_step.get(m.chat.id, {}).get("step") == "cliker_steam")
async def steam_cliker(message):
    os.startfile("C:\\Program Files (x86)\\Steam\\Steam.exe")
    global guard_x, guard_y

    offset_plus_x = 445  # смещение по X от левого верхнего угла окна
    offset_plus_y = 220  # смещение по Y от левого верхнего угла окна

    offset_login_x = 145  # смещение по X от левого верхнего угла окна
    offset_login_y = 150  # смещение по Y от левого верхнего угла окна

    offset_password_x = offset_login_x  # смещение по X от левого верхнего угла окна
    offset_password_y = offset_plus_y  # смещение по Y от левого верхнего угла окна

    offset_enter_x = 325  # смещение по X от левого верхнего угла окна
    offset_enter_y = 300  # смещение по Y от левого верхнего угла окна

    win = await wait_for_steam_open()
    if win:
        abs_x = win.left + offset_plus_x
        abs_y = win.top + offset_plus_y

        # time.sleep(2)  # время на переключение окна
        pyautogui.click(x=abs_x, y=abs_y)
        # time.sleep(1)

        login_x = win.left + offset_login_x
        login_y = win.top + offset_login_y

        guard_x = login_x+100
        guard_y = login_y+10

        pyautogui.click(x=login_x, y=login_y)
        pyautogui.click(x=login_x, y=login_y)
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.3)
        pyautogui.write('headragger', interval=0.05)

        pass_x = win.left + offset_password_x
        pass_y = win.top + offset_password_y

        pyautogui.click(x=pass_x, y=pass_y)
        pyautogui.click(x=pass_x, y=pass_y)
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.3)
        pyautogui.write('XZCXAC99M8GA',interval=0.05)

        abs_x = win.left + offset_enter_x
        abs_y = win.top + offset_enter_y

        pyautogui.click(x=abs_x, y=abs_y)
        globals.user_step[message.chat.id] = {"step": "steam_guard"}
        await bot.send_message(message.chat.id, "Введите код Steam Guard (или другой нужный код):")
    else:
        print("Окно не найдено")