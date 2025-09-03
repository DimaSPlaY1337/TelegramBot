import ctypes
import os
import time
import pyautogui

from src.Clikers.GTACliker import gta_cliker
from src.Handlers import globals
import pygetwindow as gw
from src.Handlers.ChoosingPlatform import change_pass_and_login
from src.common import bot

# проблемы:
# 1. капча спавниться пока что не пончятно как
# 2. алгоритмы проходящие капчу надо найти

guard_x = None
guard_y = None

guard_write_x = None
guard_write_y = None

win_left = None
win_top = None

counter = 0

app_list = []

@bot.message_handler(func=lambda m: globals.user_step.get(m.chat.id, {}).get("step") == "epic_guard")
async def handle_epic_guard(message):
    epic_guard = message.text  # Здесь — то, что ввел пользователь!
    print(f"Получили steam guard: {epic_guard}")
    # Здесь можно:
    # — записать steam_guard куда надо
    # — изменить шаг состояния, чтобы не ловить дальше любые сообщения
    # — продолжить логику (например, отправить steam_guard дальше или завершить процесс)
    await bot.send_message(message.chat.id, "Спасибо! Код получен.")
    pyautogui.click(x=guard_write_x, y=guard_write_y)
    pyautogui.write(epic_guard, interval=0.05)
    pyautogui.press('enter')
    # globals.user_step[message.chat.id] = {"step": "epic_capcha"}
    #
    # await epic_client(message)
    if not await is_error(430, 650, 477,700):
        await launch_prog(message)
    else:
        await bot.send_message(message.chat.id, "Код введен неверно, введите еще раз.")

async def wait_for_epic_open(title="Steam", timeout=200, interval=1):
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
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    pyautogui.write(data, interval=0.05)

@bot.message_handler(func=lambda m: globals.user_step.get(m.chat.id, {}).get("step") == "cliker_rockstar")
async def epic_cliker(message):
    os.startfile("C:\\Program Files (x86)\\Epic Games\\Launcher\\Portal\\Binaries\\Win32\\EpicGamesLauncher.exe")
    switch_to_english()
    global guard_x, guard_y, guard_write_x, guard_write_y, win_left, win_top

    offset_login_x = 584  # смещение по X от левого верхнего угла окна
    offset_login_y = 584  # смещение по Y от левого верхнего угла окна

    offset_login_cb_x = 647  # смещение по X от левого верхнего угла окна
    offset_login_cb_y = 647  # смещение по Y от левого верхнего угла окна

    offset_password_x = 665  # смещение по X от левого верхнего угла окна
    offset_password_y = 731  # смещение по Y от левого верхнего угла окна

    offset_password_cb_x = 643  # смещение по X от левого верхнего угла окна
    offset_password_cb_y = 847  # смещение по Y от левого верхнего угла окна

    # windows = gw.getAllWindows()
    # print([w.title for w in windows])

    win = await wait_for_epic_open("Epic Games Launcher")
    if win:
        win.resizeTo(1324, 1400)
        win_left = win.left
        win_top = win.top

        login_x = win.left + offset_login_x
        login_y = win.top + offset_login_y

        login_cb_x = win.left + offset_login_cb_x
        login_cb_y = win.top + offset_login_cb_y

        guard_x = win.left + 318
        guard_y = win.top + 451

        guard_write_x = win_left + 560
        guard_write_y = win_top + 748

        time.sleep(5)
        write_data(login_x, login_y, globals.data_for_reg[message.chat.id]["login"])

        pyautogui.click(x=login_cb_x, y=login_cb_y)
        pyautogui.click(x=login_cb_x, y=login_cb_y)

        if not await is_error(444, 623, 539, 632):

            pass_x = win.left + offset_password_x
            pass_y = win.top + offset_password_y

            pyautogui.click(x=pass_x, y=pass_y)
            pyautogui.click(x=pass_x, y=pass_y)

            write_data(pass_x, pass_y, globals.data_for_reg[message.chat.id]["password"])

            pass_cb_x = win.left + offset_password_cb_x
            pass_cb_y = win.top + offset_password_cb_y

            pyautogui.click(x=pass_cb_x, y=pass_cb_y)

            if not await is_error(434, 740, 508, 751):
                time.sleep(3)
                globals.user_step[message.chat.id] = {"step": "epic_guard"}
                await bot.send_message(message.chat.id, "Введите код RockStar Guard (или другой нужный код):")
            else:
                win.close()
                await change_pass_and_login(message)
        else:
            win.close()
            await change_pass_and_login(message)
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

async def epic_client(message):
    await bot.send_message(message.chat.id, "Отправьте любой символ для подтверждения что Capcha пройдена:")

@bot.message_handler(func=lambda m: globals.user_step.get(m.chat.id, {}).get("step") == "epic_capcha")
async def epic_capcha(message):
    global counter
    if counter == 0:
        click_x = win_left + 659
        click_y = win_top + 796
        pyautogui.click(x=click_x, y=click_y)
        pyautogui.click(x=click_x, y=click_y)
        counter = 1
    elif counter == 1:
        click_x = win_left + 697
        click_y = win_top + 686
        pyautogui.click(x=click_x, y=click_y)
        pyautogui.click(x=click_x, y=click_y)
        counter = 2
    elif counter == 2:
        click_x = win_left + 679
        click_y = win_top + 747
        pyautogui.click(x=click_x, y=click_y)
        pyautogui.click(x=click_x, y=click_y)
        counter = 3
    elif counter == 3:
        click_x = win_left + 672
        click_y = win_top + 812
        pyautogui.click(x=click_x, y=click_y)
        pyautogui.click(x=click_x, y=click_y)
        globals.user_step[message.chat.id] = {"step": "epic_start_game"}
    await epic_client(message)

@bot.message_handler(func=lambda m: globals.user_step.get(m.chat.id, {}).get("step") == "epic_start_game")
async def start_game(message):
    os.startfile(r"C:\Users\PC\Desktop\Grand Theft Auto V Enhanced.url")
    win = await wait_for_epic_open("Grand Theft Auto V Enhanced.url")

async def is_red(r, g, b, r_min=80, diff_g=40, diff_b=40):
    # Проверка: ярко-красный или просто любой "красный"
    return (r > r_min) and (r - g > diff_g) and (r - b > diff_b)
#!!!
async def is_green(r, g, b, g_min=80, diff_r=40, diff_b=40):
    # Проверка: ярко-зелёный или просто явно зелёный цвет
    return (g > g_min) and (g - r > diff_r) and (g - b > diff_b)

async def is_error(x1, y1, x2, y2):
    global win_left, win_top
    rc,  rg, rb = 0, 0, 0
    for x in range(x1, x2):
        for y in range(y1, y2):
            r, g, b = pyautogui.pixel(win_left + x, win_top + y)
            if await is_red(r, g, b):
                print("Здесь введен неверный пароль или логин")
                return True
    return False

async def epic_exit():
    global win_left, win_top

    offset_profile_x = 1257  # смещение по X от левого верхнего угла окна
    offset_profile_y = 78  # смещение по Y от левого верхнего угла окна

    offset_out_x = 952  # смещение по X от левого верхнего угла окна
    offset_out_y = 689  # смещение по Y от левого верхнего угла окна

    offset_accept_x = 741  # смещение по X от левого верхнего угла окна
    offset_accept_y = 774  # смещение по Y от левого верхнего угла окна

    # windows = gw.getAllWindows()
    # print([w.title for w in windows])
    # Программа
    # запуска
    # Epic
    # Games
    win = await wait_for_epic_open("Epic Games Launcher")
    win.activate()
    if win:
        win.resizeTo(1324, 1400)
        win_left = win.left
        win_top = win.top

        abs_x = win_left + offset_profile_x

        abs_y = win_top + offset_profile_y

        time.sleep(1)  # время на переключение окна
        pyautogui.click(x=abs_x, y=abs_y)

        login_x = win_left + offset_out_x
        login_y = win.top + offset_out_y

        time.sleep(1)
        pyautogui.click(x=login_x, y=login_y)

        win.close()
    else:

        print("Окно не найдено")

async def close_apps():
    global app_list
    for win in app_list:
        win.close()
    await epic_exit()

    # win = await wait_for_epic_open("Программа запуска Epic Games")
    # if win:
    #     win.close()

async def launch_prog(message):
    global app_list
    os.startfile(r"C:\Users\gamePC\Desktop\GTA`s\GTA_ES.url")
    win_gta = await wait_for_epic_open("Grand Theft Auto V Enhanced")
    app_list.append(win_gta)

    os.startfile(r"C:\Users\gamePC\Desktop\Enhanced.exe")
    win_sun = await wait_for_epic_open("Sunrise")
    app_list.append(win_sun)

    if win_gta and win_sun:
        time.sleep(20)
        await gta_cliker(message)