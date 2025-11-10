import time
from src.common import bot
import os
import src.common as common
from src.Clikers.Telegram.PlatformClicker import PlatformClicker
from src.Clikers.Telegram.input_utils import *
from src.Handlers.Telegram.rules import error_handler
import traceback


class EpicgamesClicker(PlatformClicker):
    """Кликер для EpicGames платформы"""

    def __init__(self):
        super().__init__()

    async def plat_clicker(self, message):
        """Запуск и авторизация в Epic Games"""
        try:
            await super().plat_clicker(message)
            chat_id = message.chat.id
            customer = common.get_customer(chat_id)

            os.startfile("C:\\Program Files\\Rockstar Games\\Launcher\\LauncherPatcher.exe")
            win = await wait_for_open("Rockstar Games - Sign In")

            if win:
                print("Rockstar в Epic открылся")
            else:
                print("Rockstar в Epic не открылся")

            os.startfile(
                "C:\\Program Files (x86)\\Epic Games\\Launcher\\Portal\\Binaries\\Win32\\EpicGamesLauncher.exe")
            switch_to_english()

            # Координаты элементов интерфейса
            offset_login_x = 584
            offset_login_y = 584
            offset_login_cb_x = 647
            offset_login_cb_y = 647
            offset_password_x = 665
            offset_password_y = 731
            offset_password_cb_x = 643
            offset_password_cb_y = 847

            win = await wait_for_open("Epic Games Launcher")

            if win:
                win.resizeTo(1324, 1400)
                win_left = win.left
                win_top = win.top

                login_x = win.left + offset_login_x
                login_y = win.top + offset_login_y
                login_cb_x = win.left + offset_login_cb_x
                login_cb_y = win.top + offset_login_cb_y

                time.sleep(5)
                write_data(login_x, login_y, customer.login)
                pyautogui.click(x=login_cb_x, y=login_cb_y)
                pyautogui.click(x=login_cb_x, y=login_cb_y)

                if not await is_error(customer, 444, 623, 539, 632):
                    pass_x = win.left + offset_password_x
                    pass_y = win.top + offset_password_y
                    pyautogui.click(x=pass_x, y=pass_y)
                    write_data(pass_x, pass_y, customer.password)

                    pass_cb_x = win.left + offset_password_cb_x
                    pass_cb_y = win.top + offset_password_cb_y
                    pyautogui.click(x=pass_cb_x, y=pass_cb_y)

                    if not await is_error(customer, 434, 740, 508, 751):
                        time.sleep(3)
                        customer.set_step("epic_guard")
                        await bot.send_message(
                            chat_id,
                            "Введите код Epic Games Guard:"
                        )
                    else:
                        win.close()
                        await self.change_pass_and_login(message)
                else:
                    win.close()
                    await self.change_pass_and_login(message)
            else:
                print("Окно не найдено")
                await bot.send_message(chat_id, "Не удалось найти окно Epic Games")
        except Exception as e:
            print(f"Ошибка в plat_clicker (Epic): {e}")
            print(traceback.format_exc())
            await error_handler(message.chat.id, traceback.format_exc())

    async def plat_guard(self, message):
        """Обработка ввода Epic Guard кода"""
        try:
            chat_id = message.chat.id
            customer = common.get_customer(chat_id)
            guard = message.text

            print(f"Получили epic guard: {guard}")
            await bot.send_message(chat_id, "Спасибо! Код получен.")

            # Предполагаем, что win_left и win_top сохранены в customer.clicker
            pyautogui.click(x=customer.clicker.win_left + 560, y=customer.clicker.win_top + 748)
            pyautogui.write(guard, interval=0.05)
            pyautogui.press('enter')
            time.sleep(3)

            if not await is_error(customer, 430, 650, 477, 700):
                await self.launch_prog(message)
            else:
                await bot.send_message(chat_id, "Код введен неверно, введите еще раз.")
                customer.set_step("epic_guard")
        except Exception as e:
            print(f"Ошибка в plat_guard (Epic): {e}")
            print(traceback.format_exc())
            await error_handler(message.chat.id, traceback.format_exc())

    async def launch_prog(self, message):
        """Запуск GTA через Epic Games"""
        try:
            chat_id = message.chat.id
            customer = common.get_customer(chat_id)

            # Запуск игры
            if customer.order_des["version"].lower() == "enhanced":
                os.startfile(r"C:\Users\gamePC\Desktop\GTA`s\GTA_EE.url")
            elif customer.order_des["version"].lower() == "legacy":
                os.startfile(r"C:\Users\gamePC\Desktop\GTA`s\GTA_EL.url")
            else:
                print("Ошибка выбора версии GTA")

            win_gta = await wait_for_open("Grand Theft Auto V", 200)
            self.gta = win_gta

            win_rock = await wait_for_open("Rockstar Games", 20)
            if win_rock:
                customer.set_step("rock_epic_guard")
                await bot.send_message(
                    chat_id,
                    "Введите код RockStar Guard:"
                )

            # Запуск читов
            if customer.order_des["version"].lower() == "enhanced":
                os.startfile(r"C:\Users\gamePC\Desktop\Enhanced.exe")
            elif customer.order_des["version"].lower() == "legacy":
                os.startfile(r"C:\Users\gamePC\Desktop\Legacy.exe")
            else:
                print("Ошибка выбора версии Sunrise")

            win_sun = await wait_for_open("Sunrise", 40)
            time.sleep(10)

            if win_gta and win_sun:
                end_time = time.time() + 90
                while time.time() < end_time:
                    pass

                win_gta.activate()
                win_sun.minimize()
                time.sleep(2.5)

                from src.Clikers.Telegram.GTACliker import gta_cliker_exp
                await gta_cliker_exp(message)
        except Exception as e:
            print(f"Ошибка в launch_prog (Epic): {e}")
            print(traceback.format_exc())
            await error_handler(message.chat.id, traceback.format_exc())

    async def plat_exit(self):
        """Выход из Epic Games"""
        try:
            offset_profile_x = 1257
            offset_profile_y = 78
            offset_out_x = 952
            offset_out_y = 689

            win = await wait_for_open("Epic Games Launcher")
            win.activate()

            if win:
                win.resizeTo(1324, 1400)
                win_left = win.left
                win_top = win.top

                abs_x = win_left + offset_profile_x
                abs_y = win_top + offset_profile_y
                time.sleep(1)
                pyautogui.click(x=abs_x, y=abs_y)

                login_x = win_left + offset_out_x
                login_y = win.top + offset_out_y
                time.sleep(1)
                pyautogui.click(x=login_x, y=login_y)
                win.close()
            else:
                print("Окно не найдено")
        except Exception as e:
            print(f"Ошибка в plat_exit (Epic): {e}")

    async def close_apps(self, message):
        """Закрытие всех приложений Epic"""
        try:
            # Выход из GTA
            pyautogui.hotkey('alt', 'f4')
            if self.gta is not None:
                self.gta.activate()
                time.sleep(7)
                keyboard_press_key('enter')
                print("Вышли из GTA")

            time.sleep(5)
            print("Закрываем Epic")
            await self.plat_exit()
            time.sleep(1)
            await self.close_sunrise()
            print("Цикл завершён")

            await super().close_apps(message)
        except Exception as e:
            print(f"Ошибка в close_apps (Epic): {e}")
            print(traceback.format_exc())
            await error_handler(message.chat.id, traceback.format_exc())


# Обработчик для Epic Guard
@bot.message_handler(func=lambda m: common.get_customer(m.chat.id).get_step() == "epic_guard")
async def handle_epic_guard(message):
    """Обработчик ввода Epic Guard"""
    try:
        chat_id = message.chat.id
        customer = common.get_customer(chat_id)

        if customer.clicker and isinstance(customer.clicker, EpicgamesClicker):
            await customer.clicker.plat_guard(message)
    except Exception as e:
        print(f"Ошибка в handle_epic_guard: {e}")
        await error_handler(message.chat.id, traceback.format_exc())


# Обработчик для Rockstar Guard в Epic
@bot.message_handler(func=lambda m: common.get_customer(m.chat.id).get_step() == "rock_epic_guard")
async def handle_rock_epic_guard(message):
    """Обработчик ввода Rockstar Guard в Epic"""
    try:
        chat_id = message.chat.id
        customer = common.get_customer(chat_id)

        if customer.clicker and isinstance(customer.clicker, EpicgamesClicker):
            await customer.clicker.rockstar_cliker(message, message.text, ignore_launch=True)
    except Exception as e:
        print(f"Ошибка в handle_rock_epic_guard: {e}")
        await error_handler(message.chat.id, traceback.format_exc())