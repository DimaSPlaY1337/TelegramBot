from abc import ABC, abstractmethod
from src.Clikers.input_utils import *
from src.common import *

class PlatformClicker(ABC):

    def __init__(self):
        self.win_left = 0
        self.win_top = 0
        self.gta = None
        self.is_changing_data = False

    async def plat_clicker(self, message):
        global type_of_soft

        if order_des[message.chat.id]["amount"].isdigit():
            if int(order_des[message.chat.id]["amount"]) >= 75000000:
                type_of_soft = "Exp"
            else:
                type_of_soft = "Free"
        else:
            type_of_soft = "Free"

    @abstractmethod
    async def plat_guard(self, message):
        pass

    @abstractmethod
    async def launch_prog(self, message):
        pass

    @abstractmethod
    async def plat_exit(self):
        pass

    @abstractmethod
    async def close_apps(self):
        pass

    async def close_sunrise(self):
        win = await wait_for_open("Sunrise", 40)
        time.sleep(1)
        win.activate()
        pyautogui.hotkey('alt', 'f4')
        time.sleep(0.3)
        pyautogui.hotkey('alt', 'f4')
        time.sleep(0.3)
        pyautogui.hotkey('alt', 'f4')

    @bot.message_handler(func=lambda m: user_step.get(m.chat.id, {}).get("step") == "rock_steam_guard")
    async def rockstar_cliker(self, message):
        global win_left, win_top, sign_in_rock_button

        rock_guard = message.text
        print(f"Получили rock guard: {rock_guard}")
        await bot.send_message(message.chat.id, "Спасибо! Код получен.")

        pyautogui.click(x=win_left + 233, y=win_top + 475)
        time.sleep(0.2)
        pyautogui.write(rock_guard, interval=0.05)
        pyautogui.click(x=win_left + 527, y=sign_in_rock_button)

        time.sleep(6)
        if await is_error(368, 508, 388, 511):  # узнать коор ошибки при вводе кода
            await bot.send_message(message.chat.id, "Код введен неверно, введите еще раз.")
            sign_in_rock_button = win_top + 622
        else:
            await self.rockstar_acceptance(message)

    async def rockstar_search(self, message):
        global win_left, win_top, sign_in_rock_button

        win_rock = await wait_for_open("Rockstar Games - Sign In", 100)
        if win_rock:
            win_left = win_rock.left
            win_top = win_rock.top
            sign_in_rock_button = win_top + 601

            user_step[message.chat.id] = {"step": "rock_steam_guard"}
            await bot.send_message(message.chat.id, "Введите код RockStar Guard (или другой нужный код):")
        else:
            await self.launch_prog(message)

    async def rockstar_acceptance(self, message):
        global win_left, win_top

        time.sleep(12)
        win_rock = await wait_for_open("Rockstar Games Launcher", 100)
        if win_rock:
            win_rock.resizeTo(1024, 600)
            time.sleep(0.5)
            win_rock.activate()
            time.sleep(0.5)

            win_left = win_rock.left
            win_top = win_rock.top

            pyautogui.click(x=win_left + 831, y=win_top + 412)  # узнать координаты

        time.sleep(5)
        await self.launch_prog(message)

    async def change_pass_and_login(self, message):
        is_changing_data = True
        user_step[message.chat.id] = {"step": "login"}
        await bot.send_message(message.chat.id, "Введите ваш логин:")

    win_left = 0
    win_top = 0
    gta = None
    is_changing_data = False