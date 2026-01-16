from abc import ABC, abstractmethod
import os
from src.Clikers.Telegram.input_utils import *
from src.common import bot
import src.common as common
from src.Handlers.Telegram.rules import error_handler
import traceback
import time


class PlatformClicker(ABC):
    """Базовый класс для кликеров платформ"""

    def __init__(self):
        self.win_left = 0
        self.win_top = 0
        self.gta = None
        self.is_changing_data = False
        self.sign_in_rock_button = 0

    async def plat_clicker(self, message):
        """Основной метод запуска кликера"""
        try:
            chat_id = message.chat.id
            customer = common.get_customer(chat_id)

            # Определяем тип софта
            if customer.order_des["amount"].isdigit():
                if int(customer.order_des["amount"]) >= 30000000:
                    customer.type_of_soft = "Exp"
                else:
                    customer.type_of_soft = "Free"
            else:
                customer.type_of_soft = "Free"

            if customer.order_des["unlocks"] == "super unlocks":
                customer.type_of_soft = "Exp"

            # Запускаем beSkip
            win_be = None
            # if not await wait_for_open("C:\\Users\\gamePC\\Desktop\\beSkip.exe", 3):
            #     os.startfile(r"C:\Users\gamePC\Desktop\beSkip.exe", 'runas')
            #     win_be = await wait_for_open("C:\\Users\\gamePC\\Desktop\\beSkip.exe")
            # else:
            #     win_be = await wait_for_open("C:\\Users\\gamePC\\Desktop\\beSkip.exe")
        except Exception as e:
            print(f"Ошибка в plat_clicker: {e}")
            print(traceback.format_exc())
            await error_handler(message.chat.id, traceback.format_exc())

    @abstractmethod
    async def plat_guard(self, message):
        """Обработка ввода Guard кода"""
        pass

    @abstractmethod
    async def launch_prog(self, message):
        """Запуск программы/игры"""
        pass

    @abstractmethod
    async def plat_exit(self):
        """Выход из платформы"""
        pass

    async def close_apps(self, message):
        """Закрытие всех приложений"""
        try:
            chat_id = message.chat.id
            customer = common.get_customer(chat_id)

            if customer.type_of_soft == "Exp":
                await self.close_sunrise()

            await bot.send_message(chat_id, "✅ Процесс завершен!")
        except Exception as e:
            print(f"Ошибка в close_apps: {e}")
            print(traceback.format_exc())
            await error_handler(message.chat.id, traceback.format_exc())

    async def close_sunrise(self):
        """Закрытие Sunrise"""
        try:
            win = await wait_for_open("Sunrise", 5)
            if win:
                time.sleep(1)
                win.activate()
                pyautogui.hotkey('alt', 'f4')
                time.sleep(0.3)
                pyautogui.hotkey('alt', 'f4')
                time.sleep(0.3)
                pyautogui.hotkey('alt', 'f4')
        except Exception as e:
            print(f"Ошибка при закрытии Sunrise: {e}")

    async def rockstar_cliker(self, message, guard_code, ignore_launch=False):
        """Обработка Rockstar Guard"""
        try:
            chat_id = message.chat.id
            customer = common.get_customer(chat_id)

            print(f"Получили rock guard: {guard_code}")
            pyautogui.FAILSAFE = False

            await bot.send_message(chat_id, "Спасибо! Код получен.")

            pyautogui.click(x=self.win_left + 233, y=self.win_top + 475)
            time.sleep(0.2)
            pyautogui.write(guard_code, interval=0.05)
            pyautogui.click(x=self.win_left + 527, y=self.sign_in_rock_button)
            time.sleep(6)

            if await is_error(customer, 368, 508, 388, 511):
                await bot.send_message(chat_id, "Код введен неверно, введите еще раз.")
                self.sign_in_rock_button = self.win_top + 622
                customer.set_step("rockstar_guard_retry")
            else:
                await self.rockstar_acceptance(message, ignore_launch)
        except Exception as e:
            print(f"Ошибка в rockstar_cliker: {e}")
            print(traceback.format_exc())
            await error_handler(message.chat.id, traceback.format_exc())

    async def rockstar_search(self, message, wait_time=100, ignore_launch=False):
        """Поиск окна Rockstar"""
        try:
            chat_id = message.chat.id
            customer = common.get_customer(chat_id)

            win_rock = await wait_for_open("Rockstar Games - Sign In", wait_time)
            if win_rock:
                self.win_left = win_rock.left
                self.win_top = win_rock.top
                self.sign_in_rock_button = self.win_top + 601

                await bot.send_message(
                    chat_id,
                    "Введите код RockStar Guard (или другой нужный код):"
                )
                customer.set_step("rockstar_guard")
            elif not ignore_launch:
                await self.launch_prog(message)
        except Exception as e:
            print(f"Ошибка в rockstar_search: {e}")
            print(traceback.format_exc())
            await error_handler(message.chat.id, traceback.format_exc())

    async def rockstar_acceptance(self, message, ignore_launch=False):
        """Принятие соглашений Rockstar"""
        try:
            time.sleep(12)
            win_rock = await wait_for_open("Rockstar Games Launcher", 20) or \
                       await wait_for_open("Rockstar Games - Sign In", 20)

            if win_rock:
                win_rock.resizeTo(1024, 600)
                time.sleep(0.5)
                win_rock.activate()
                time.sleep(0.5)
                pyautogui.click(x=win_rock.left + 831, y=win_rock.top + 412)
                time.sleep(7)
                pyautogui.click(x=win_rock.left + 831, y=win_rock.top + 412)
                time.sleep(7)
                pyautogui.click(x=win_rock.left + 831, y=win_rock.top + 412)

                if not ignore_launch:
                    time.sleep(5)
                    await self.launch_prog(message)
        except Exception as e:
            print(f"Ошибка в rockstar_acceptance: {e}")
            print(traceback.format_exc())

    async def change_pass_and_login(self, message):
        """Изменение логина и пароля"""
        try:
            chat_id = message.chat.id
            customer = common.get_customer(chat_id)

            customer.is_changing_data = True
            customer.set_step("login")
            await bot.send_message(chat_id, "Введите ваш логин:")
        except Exception as e:
            print(f"Ошибка в change_pass_and_login: {e}")
            print(traceback.format_exc())
            await error_handler(message.chat.id, traceback.format_exc())

    # Обработчик для Rockstar Guard
    @bot.message_handler(func=lambda m: common.get_customer(m.chat.id).get_step() == "rockstar_guard")
    async def handle_rockstar_guard(message):
        """Обработчик ввода Rockstar Guard"""
        try:
            chat_id = message.chat.id
            customer = common.get_customer(chat_id)

            if customer.clicker:
                await customer.clicker.plat_guard(message)
        except Exception as e:
            print(f"Ошибка в handle_rockstar_guard: {e}")
            await error_handler(message.chat.id, traceback.format_exc())

    async def create_json(self, message):
        # --------------------------
        # file_path = r"C:\Users\%USERNAME%\Documents\Cherax\Lua\GTA5SERVICE\Boosting.json"
        file_path = r"C:\Users\%USERNAME%\Documents\Boosting.json"
        # os.path.expandvars(), который автоматически заменит переменную окружения на имя текущего пользователя
        expanded_path = os.path.expandvars(file_path)

        # Загрузка JSON
        with open(expanded_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # if "amount": "100000000" ==  cash + chips ( где cash<= 25000000, chips = amount-cash)
            data['Chips']['Loop_Amount'] = int(customer.order_des["amount"])
            data['Chips']['Limiter'] = 500000000
            data['Ranks']['Player'] = customer.order_des["levels"]
            data['Unlocks']['Weapons'] = True
            data['Unlocks']['Vehicles'] = True
        # self.order_des = {
        #     "version": "не задано",
        #     "amount": "не задано",
        #     "levels": "не задано",
        #     "unlocks": "не задано"
        # }
        # Изменение значений в разных секциях
        # Сохранение обратно в тот же файл
        with open(expanded_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=3)
        # -------------------------------