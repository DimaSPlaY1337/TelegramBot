from abc import ABC, abstractmethod
from src.Clikers.Digiseller.input_utils import *
from src.Handlers.Digiseller.IO_utils import *


class PlatformClicker(ABC):

    def __init__(self):
        self.win_left = 0
        self.win_top = 0
        self.gta = None
        self.is_changing_data = False
        self.sign_in_rock_button = 0

    async def plat_clicker(self, token, dialog_id, message_text, customer):
        if customer.order_des["amount"].isdigit():
            if int(customer.order_des["amount"]) >= 75000000:
                customer.type_of_soft = "Exp"
            else:
                customer.type_of_soft = "Free"
        else:
            customer.type_of_soft = "Free"

    @abstractmethod
    async def plat_guard(self, token, dialog_id, message_text, customer):
        pass

    @abstractmethod
    async def launch_prog(self, token, dialog_id, message_text, customer):
        pass

    @abstractmethod
    async def plat_exit(self):
        pass

    async def close_apps(self, token):
        await finish_current_order(token)

    async def close_sunrise(self):
        win = await wait_for_open("Sunrise", 40)
        time.sleep(1)
        win.activate()
        pyautogui.hotkey('alt', 'f4')
        time.sleep(0.3)
        pyautogui.hotkey('alt', 'f4')
        time.sleep(0.3)
        pyautogui.hotkey('alt', 'f4')

    # @bot.message_handler(func=lambda m: common.user_step.get(m.chat.id, {}).get("step") == "rock_steam_guard")
    async def rockstar_cliker(self, token, dialog_id, message_text, customer, ignore_launch):
        print(f"Получили rock guard: {message_text}")
        await send_message(token, dialog_id, "Спасибо! Код получен.")

        pyautogui.click(x=self.win_left + 233, y=self.win_top + 475)
        time.sleep(0.2)
        pyautogui.write(message_text, interval=0.05)
        pyautogui.click(x=self.win_left + 527, y=self.sign_in_rock_button)

        time.sleep(6)
        if await is_error(customer,368, 508, 388, 511):  # узнать коор ошибки при вводе кода
            await send_message(token, dialog_id, "Код введен неверно, введите еще раз.")
            self.sign_in_rock_button = self.win_top + 622

            guard = await wait_for_message(token, dialog_id)
            await self.rockstar_cliker(token, dialog_id, guard, customer, ignore_launch)
        else:
            await self.rockstar_acceptance(token, dialog_id, message_text, customer, ignore_launch)

    async def rockstar_search(self, token, dialog_id, message_text, customer, wait_time=100, ignore_launch=False):
        win_rock = await wait_for_open("Rockstar Games - Sign In", wait_time)
        if win_rock:
            self.win_left = win_rock.left
            self.win_top = win_rock.top
            self.sign_in_rock_button = self.win_top + 601

            await send_message(token, dialog_id, "Введите код RockStar Guard (или другой нужный код):")
            guard = await wait_for_message(token, dialog_id)
            await self.rockstar_cliker(token, dialog_id, guard, customer, ignore_launch)
        elif not ignore_launch:
            await self.launch_prog(token, dialog_id, message_text, customer)

    async def rockstar_acceptance(self, token, dialog_id, message_text, customer, ignore_launch):
        time.sleep(12)
        win_rock = await wait_for_open("Rockstar Games Launcher", 100)
        if win_rock:
            win_rock.resizeTo(1024, 600)
            time.sleep(0.5)
            win_rock.activate()
            time.sleep(0.5)

            pyautogui.click(x=win_rock.left + 831, y=win_rock.top + 412)  # узнать координаты

        if not ignore_launch:
            time.sleep(5)
            await self.launch_prog(token, dialog_id, message_text, customer)

    async def change_pass_and_login(self, token, dialog_id, message_text, customer):
        self.is_changing_data = True
        customer.user_step = "login"
        await send_message(token, dialog_id, "Введите ваш логин:")