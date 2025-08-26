import pyautogui
import time
from pynput.keyboard import Controller, Key

def press_key(key, times=1):
    for _ in range(times):
        pyautogui.press(key)
        time.sleep(0.5) # небольшая пауза между нажатиями

def hold_key(key, duration=1.0):
    pyautogui.keyDown(key)
    time.sleep(duration)
    pyautogui.keyUp(key)

def write_text(text):
    pyautogui.typewrite(str(text), interval=0.5)

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

    # enter
    press_key('enter')

    # 1 down
    press_key('down', 1)
    press_key('enter')

    # write order
    order = 75000000
    keyboard.type(str(order))
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    press_key('enter')

    time.sleep(0.5)

    # down
    press_key('down')
    press_key('enter')

    # write(200000000-75000000)
    result = str(300000000 - order)
    keyboard.type(result)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

    time.sleep(0.5)

    # backspace
    press_key('backspace')

    # 5 down
    press_key('down', 5)
    press_key('enter')

    time.sleep(0.5)
    # (62, 65, 73)
    target_color = (62, 65, 73)
    x = 2345
    y = 694
    while True:
        # Считываем цвет пикселя
        pixel_color = pyautogui.pixel(x, y)
        print(f"Текущий цвет: {pixel_color}")

        # Проверка цвета
        if pixel_color == target_color:
            print("Цвет стал целевым!")
            break

        time.sleep(0.2)  # небольшая задержка, чтобы не грузить процессор
    # check red label disapear, while lable != black: wait
    # (Это требует проверки содержимого экрана, не реализовано простым pyautogui)

    # 4 up
    press_key('up', 4)

    # enter
    press_key('enter')
    press_key('enter')
    target_color = (62, 65, 73)
    x = 2411
    y = 568
    while True:
        # Считываем цвет пикселя
        pixel_color = pyautogui.pixel(x, y)
        print(f"Текущий цвет: {pixel_color}")

        # Проверка цвета
        if pixel_color == target_color:
            print("Цвет стал целевым!")
            break

    # backspace
    press_key('backspace')
    press_key('backspace')

    # 2 down
    press_key('down', 2)
    press_key('enter')

    # write level
    order = 1000
    keyboard.type(str(order))
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    time.sleep(0.5)

    # write_text('level')
    # press_key('enter')

    # 1 down
    press_key('down', 1)
    press_key('enter')

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

    # clava "o"
    write_text('o')

    # 15 сек ждем
    time.sleep(15)

    # backspace
    press_key('backspace')
    press_key('backspace')

    # 8 up
    press_key('up', 8)
    press_key('enter')

    # 1 up for legacy
    press_key('up', 1)

    # 2 up for Enhanced
    press_key('up', 2)
    press_key('enter')

    # clava f5
    press_key('f5')

    # Скрин окна GTA:
    screenshot = pyautogui.screenshot()
    screenshot.save('gta_screen.png')
