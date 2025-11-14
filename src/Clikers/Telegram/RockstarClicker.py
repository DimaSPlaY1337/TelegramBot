import time
from src.common import bot
import os
import src.common as common
from src.Clikers.Telegram.PlatformClicker import PlatformClicker
from src.Clikers.Telegram.input_utils import *
from src.Clikers.Telegram.Cherax_cliker import c_cliker
from src.Handlers.Telegram.rules import error_handler
import traceback


class RockstarClicker(PlatformClicker):
    """Кликер для Rockstar платформы"""

    def __init__(self):
        super().__init__()

    async def plat_clicker(self, message):
        """Запуск и авторизация в Rockstar"""
        try:
            await super().plat_clicker(message)
            chat_id = message.chat.id
            customer = common.get_customer(chat_id)

            os.startfile("C:\\Program Files\\Rockstar Games\\Launcher\\LauncherPatcher.exe")
            switch_to_english()

            # Координаты элементов интерфейса
            offset_password_x = 250
            offset_password_y = 420
            offset_enter_x = 520
            offset_enter_y = 520

            time.sleep(0.5)
            win = await wait_for_open("Rockstar Games - Sign In", 100)

            if win:
                win.resizeTo(700, 800)
                time.sleep(0.3)
                win.activate()
                time.sleep(0.2)

                customer.clicker.win_left = win.left
                customer.clicker.win_top = win.top

                # Ввод логина
                login_x = win.left + 250
                login_y = win.top + 350
                time.sleep(3)
                write_data(login_x, login_y, customer.login)

                # Ввод пароля
                pass_x = win.left + offset_password_x
                pass_y = win.top + offset_password_y
                write_data(pass_x, pass_y, customer.password)

                # Кнопка входа
                abs_x = win.left + offset_enter_x
                abs_y = win.top + offset_enter_y
                pyautogui.click(x=abs_x, y=abs_y)
                time.sleep(4)

                if (not await is_error(customer, 101, 186, 141, 204) and
                        not await is_error(customer, 123, 351, 134, 359)):
                    time.sleep(5)
                    win = await wait_for_open("Rockstar Games - Sign In", 10) or None

                    if win:
                        customer.clicker.win_top = win.top
                        customer.clicker.win_left = win.left
                        customer.set_step("rockstar_guard")
                        await bot.send_message(
                            chat_id,
                            "Введите код RockStar Guard:"
                        )
                    else:
                        if customer.type_of_soft == "Exp":
                            await self.launch_prog(message)
                        else:
                            await c_cliker(message)
                else:
                    win.close()
                    await self.change_pass_and_login(message)
            else:
                print("Окно не найдено")
                await bot.send_message(chat_id, "Не удалось найти окно Rockstar")
        except Exception as e:
            print(f"Ошибка в plat_clicker (Rockstar): {e}")
            print(traceback.format_exc())
            await error_handler(message.chat.id, traceback.format_exc())

    async def plat_guard(self, message):
        """Обработка ввода Rockstar Guard кода"""
        try:
            chat_id = message.chat.id
            customer = common.get_customer(chat_id)
            guard = message.text

            print(f"Получили rockstar guard: {guard}")
            await bot.send_message(chat_id, "Спасибо! Код получен.")

            pyautogui.click(x=customer.clicker.win_left + 318, y=customer.clicker.win_top + 451)
            pyautogui.write(guard, interval=0.05)
            pyautogui.click(x=customer.clicker.win_left + 538, y=customer.clicker.win_top + 563)

            # 2-step verification
            pyautogui.click(x=customer.clicker.win_left + 522, y=customer.clicker.win_top + 517)

            if customer.type_of_soft == "Exp":
                if not await is_error(customer, 430, 650, 440, 660):
                    await self.launch_prog(message)
                else:
                    await bot.send_message(chat_id, "Код введен неверно, введите еще раз.")
                    customer.set_step("rockstar_guard")
            else:
                if not await is_error(customer, 430, 650, 440, 660):
                    await c_cliker(message)
                else:
                    await bot.send_message(chat_id, "Код введен неверно, введите еще раз.")
                    customer.set_step("rockstar_guard")
        except Exception as e:
            print(f"Ошибка в plat_guard (Rockstar): {e}")
            print(traceback.format_exc())
            await error_handler(message.chat.id, traceback.format_exc())

    async def launch_prog(self, message):
        """Запуск GTA через Rockstar"""
        try:
            chat_id = message.chat.id
            customer = common.get_customer(chat_id)

            # Запуск игры
            if customer.order_des["version"].lower() == "enhanced":
                os.startfile(r"C:\Users\gamePC\Desktop\GTA`s\GTA_RE.lnk")
            elif customer.order_des["version"].lower() == "legacy":
                os.startfile(r"C:\Users\gamePC\Desktop\GTA`s\GTA_RL.lnk")
            else:
                print("Ошибка выбора версии GTA")

            time.sleep(7)
            await self.rockstar_acceptance(message, True)
            # win_rock = await wait_for_open("Rockstar Games Launcher", 10)

            win_gta = await wait_for_open("Grand Theft Auto V", 200)
            self.gta = win_gta

            # Запуск читов
            os.startfile(r"C:\Users\gamePC\Desktop\Sunrise.exe")

            win_sun = await wait_for_open("Sunrise", 40)
            found = False
            time.sleep(10)

            if win_gta and win_sun:
                end_time = time.time() + 90
                search_gray_window(found)
                win_gta.activate()
                win_sun.minimize()
                time.sleep(2.5)

                from src.Clikers.Telegram.GTACliker import gta_cliker_exp
                await gta_cliker_exp(message)
        except Exception as e:
            print(f"Ошибка в launch_prog (Rockstar): {e}")
            print(traceback.format_exc())
            await error_handler(message.chat.id, traceback.format_exc())

    async def plat_exit(self):
        """Выход из Rockstar"""
        try:
            offset_profile_x = 1031
            offset_profile_y = 67
            offset_out_x = 969
            offset_out_y = 336

            win = await wait_for_open("Rockstar Games Launcher")
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
        except Exception as e:
            print(f"Ошибка в plat_exit (Rockstar): {e}")

    async def close_apps(self, message):
        """Закрытие всех приложений Rockstar"""
        try:
            # Выход из GTA
            pyautogui.hotkey('alt', 'f4')
            if self.gta is not None:
                self.gta.activate()
                time.sleep(7)
                keyboard_press_key('enter')
                print("Вышли из GTA")

            time.sleep(5)
            print("Закрываем rock1")
            await self.plat_exit()
            time.sleep(1)

            win_cherax = await wait_for_open("Cherax Loader", 5) or \
                         await find_window_by_size(900, 600, timeout=5)
            if win_cherax is not None:
                win_cherax.close()

            print("Цикл завершён")
            await super().close_apps(message)
        except Exception as e:
            print(f"Ошибка в close_apps (Rockstar): {e}")
            print(traceback.format_exc())
            await error_handler(message.chat.id, traceback.format_exc())


# Обработчик для Rockstar Guard
@bot.message_handler(func=lambda m: common.get_customer(m.chat.id).get_step() == "rockstar_guard")
async def handle_rockstar_guard(message):
    """Обработчик ввода Rockstar Guard"""
    try:
        chat_id = message.chat.id
        customer = common.get_customer(chat_id)

        if customer.clicker and isinstance(customer.clicker, RockstarClicker):
            await customer.clicker.plat_guard(message)
    except Exception as e:
        print(f"Ошибка в handle_rockstar_guard: {e}")
        await error_handler(message.chat.id, traceback.format_exc())