import ctypes

import pyautogui
import time
import keyboard
from pynput.keyboard import Controller, Key

# def press_key(key, times=1):
#     for _ in range(times):
#         pyautogui.press(key)
#         time.sleep(0.25) # небольшая пауза между нажатиями

def press_key(key, times=1):
    for _ in range(times):
        keyboard.press_and_release(key)
        time.sleep(2)

def hold_key(key, duration=1.0):
    pyautogui.keyDown(key)
    time.sleep(duration)
    pyautogui.keyUp(key)

def write_text(text):
    pyautogui.typewrite(str(text), interval=0.5)

def write_text(text):
    keyboard.write(text, delay=0.05)

# async def gta_cliker(message):
#     switch_to_english()
#     keyboard = Controller()
#     # Последовательность команд (по сообщениям)
#     # f5
#     press_key('f5')
#     # 4 down
#
#     press_key('down')
#     press_key('down')
#     press_key('down')
#     press_key('down')
#     # enter
#     press_key('enter')
#
#     # enter
#     press_key('enter')
#     # enter
#     press_key('enter')
#
#     # 1 down
#     press_key('down', 1)
#     press_key('enter')
#
#     # write order
#     order = 75000000
#     keyboard.type(str(order))
#     keyboard.press(Key.enter)
#     keyboard.release(Key.enter)
#     press_key('enter')
#
#     time.sleep(0.5)
#
#     # down
#     press_key('down')
#     press_key('enter')
#
#     # write(200000000-75000000)
#     result = str(125000000 - order)
#     keyboard.type(result)
#     keyboard.press(Key.enter)
#     keyboard.release(Key.enter)
#
#     time.sleep(0.5)
#
#     # backspace
#     press_key('backspace')
#
#     # 5 down
#     press_key('down', 5)
#     press_key('enter')
#
#     time.sleep(0.5)
#     # (62, 65, 73)
#     target_color = (62, 65, 73)
#     x = 2345
#     y = 694
#     while True:
#         # Считываем цвет пикселя
#         pixel_color = pyautogui.pixel(x, y)
#         print(f"Текущий цвет: {pixel_color}")
#
#         # Проверка цвета
#         if pixel_color == target_color:
#             print("Цвет стал целевым!")
#             break
#
#         time.sleep(0.2)  # небольшая задержка, чтобы не грузить процессор
#     # check red label disapear, while lable != black: wait
#     # (Это требует проверки содержимого экрана, не реализовано простым pyautogui)
#
#     # 4 up
#     press_key('up', 4)
#
#     # enter
#     press_key('enter')
#     press_key('enter')
#     target_color = (62, 65, 73)
#     x = 2411
#     y = 568
#     while True:
#         # Считываем цвет пикселя
#         pixel_color = pyautogui.pixel(x, y)
#         print(f"Текущий цвет: {pixel_color}")
#
#         # Проверка цвета
#         if pixel_color == target_color:
#             print("Цвет стал целевым!")
#             break
#
#     # backspace
#     press_key('backspace')
#     press_key('backspace')
#
#     # 2 down
#     press_key('down', 2)
#     press_key('enter')
#
#     # write level
#     order = 1000
#     keyboard.type(str(order))
#     keyboard.press(Key.enter)
#     keyboard.release(Key.enter)
#     time.sleep(0.5)
#
#     # write_text('level')
#     # press_key('enter')
#
#     # 1 down
#     press_key('down', 1)
#     press_key('enter')
#
#     # backspace
#     press_key('backspace')
#
#     # down 2
#     press_key('down', 2)
#     press_key('enter')
#
#     # up 1
#     press_key('up', 1)
#     press_key('enter')
#
#     # down 1
#     press_key('down', 1)
#     press_key('enter')
#
#     # clava "o"
#     write_text('o')
#
#     # 15 сек ждем
#     time.sleep(15)
#
#     # backspace
#     press_key('backspace')
#     press_key('backspace')
#
#     # 8 up
#     press_key('up', 8)
#     press_key('enter')
#
#     # 1 up for legacy
#     press_key('up', 1)
#
#     # 2 up for Enhanced
#     press_key('up', 2)
#     press_key('enter')
#
#     # clava f5
#     press_key('f5')
#
#     # Скрин окна GTA:
#     screenshot = pyautogui.screenshot()
#     screenshot.save('gta_screen.png')

async def gta_cliker(message):
    switch_to_english()
    # f5
    press_key('f5')
    # 4 down
    press_key('down', 5)
    # 3 enter
    press_key('enter', 3)

    # 1 down + enter
    press_key('down')
    press_key('enter')

    # write order
    order = 75000000
    write_text(str(order))
    press_key('enter')

    time.sleep(0.5)

    # down + enter
    press_key('down')
    press_key('enter')

    # write(200000000-75000000)
    result = str(125000000 - order)
    write_text(result)
    press_key('enter')

    time.sleep(0.5)

    # backspace
    press_key('backspace')

    # 5 down + enter
    press_key('down', 5)
    press_key('enter')

    time.sleep(0.5)

    # Проверка цвета (1)
    target_color = (62, 65, 73)
    x, y = 2345, 694
    while True:
        pixel_color = pyautogui.pixel(x, y)
        print(f"Текущий цвет: {pixel_color}")
        if pixel_color == target_color:
            print("Цвет стал целевым!")
            break
        time.sleep(0.2)

    # 4 up + 2 enter
    press_key('up', 4)
    press_key('enter', 2)

    # Проверка цвета (2)
    target_color = (62, 65, 73)
    x, y = 2411, 568
    while True:
        pixel_color = pyautogui.pixel(x, y)
        print(f"Текущий цвет: {pixel_color}")
        if pixel_color == target_color:
            print("Цвет стал целевым!")
            break
        time.sleep(0.2)

    # 2 backspace
    press_key('backspace', 2)

    # 2 down + enter
    press_key('down', 2)
    press_key('enter')

    # write level, enter, пауза
    order = 1000
    write_text(str(order))
    press_key('enter')
    time.sleep(0.5)

    # 1 down + enter
    press_key('down')
    press_key('enter')

    # backspace
    press_key('backspace')

    # 2 down + enter
    press_key('down', 2)
    press_key('enter')

    # up 1 + enter
    press_key('up')
    press_key('enter')

    # down 1 + enter
    press_key('down')
    press_key('enter')

    # буква "o"
    write_text('o')

    # 15 сек пауза
    time.sleep(15)

    # 2 backspace
    press_key('backspace', 2)

    # 8 up + enter
    press_key('up', 8)
    press_key('enter')

    # 1 up, 2 up + enter
    press_key('up')
    press_key('up', 2)
    press_key('enter')

    # f5
    press_key('f5')

    # Скриншот
    screenshot = pyautogui.screenshot()
    screenshot.save('gta_screen.png')

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