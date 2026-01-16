import time
import os
from src.common import bot
import src.common as common
from src.Clikers.Telegram.PlatformClicker import PlatformClicker
from src.Clikers.Telegram.input_utils import *
from src.Clikers.Telegram.Cherax_cliker import c_cliker
from src.Handlers.Telegram.rules import error_handler
import traceback


class SteamClicker(PlatformClicker):
    """Кликер для Steam платформы"""

    def __init__(self):
        super().__init__()

    async def plat_clicker(self, message):
        """Запуск и авторизация в Steam"""
        try:
            await super().plat_clicker(message)
            chat_id = message.chat.id
            customer = common.get_customer(chat_id)

            os.startfile("C:\\Program Files\\Rockstar Games\\Launcher\\LauncherPatcher.exe")
            time.sleep(10)

            os.startfile("C:\\Program Files (x86)\\Steam\\Steam.exe")
            switch_to_english()

            # Координаты элементов интерфейса Steam
            offset_plus_x = 445
            offset_plus_y = 220
            offset_login_x = 145
            offset_login_y = 150
            offset_password_x = offset_login_x
            offset_password_y = offset_plus_y
            offset_enter_x = 325
            offset_enter_y = 300

            time.sleep(0.5)
            win = await wait_for_open("Sign in to Steam", 20) or \
                  await wait_for_open("Войти в Steam", 20)

            if win:
                win.resizeTo(705, 440)
                time.sleep(0.2)
                win.activate()

                customer.clicker.win_left = win.left
                customer.clicker.win_top = win.top

                # Клик на "Добавить аккаунт"
                abs_x = win.left + offset_plus_x
                abs_y = win.top + offset_plus_y
                time.sleep(0.5)
                pyautogui.click(x=abs_x, y=abs_y)

                # Ввод логина
                login_x = win.left + offset_login_x
                login_y = win.top + offset_login_y
                win.activate()
                time.sleep(0.2)
                pyautogui.click(x=login_x, y=login_y)
                pyautogui.click(x=login_x, y=login_y)
                write_data(login_x, login_y, customer.login)

                # Ввод пароля
                pass_x = win.left + offset_password_x
                pass_y = win.top + offset_password_y
                win.activate()
                time.sleep(0.2)
                pyautogui.click(x=pass_x, y=pass_y)
                pyautogui.click(x=pass_x, y=pass_y)
                write_data(pass_x, pass_y, customer.password)

                # Кнопка входа
                pass_cb_x = win.left + offset_enter_x
                pass_cb_y = win.top + offset_enter_y
                pyautogui.click(x=pass_cb_x, y=pass_cb_y)

                # Клик на "Добавить код"
                add_kode_x = win.left + 352
                add_kode_y = win.top + 320
                pyautogui.click(x=add_kode_x, y=add_kode_y)

                if not await is_error(customer, 51, 339, 121, 352):
                    time.sleep(5)
                    win = await wait_for_open("Sign in to Steam", 5) or \
                          await wait_for_open("Войти в Steam", 5)

                    if win:
                        customer.clicker.win_top = win.top
                        customer.clicker.win_left = win.left
                        customer.set_step("steam_guard")
                        await bot.send_message(
                            chat_id,
                            "Введите код Steam Guard:"
                        )
                    else:
                        # Guard не нужен
                        if customer.type_of_soft == "Exp":
                            self.start_game(customer)
                            await self.steam_EULA()
                            time.sleep(5)
                            await self.rockstar_search(message)
                        else:
                            await c_cliker(message)
                else:
                    win.close()
                    await self.change_pass_and_login(message)
            else:
                print("Окно Steam не найдено")
                await bot.send_message(chat_id, "Не удалось найти окно Steam")
        except Exception as e:
            print(f"Ошибка в plat_clicker (Steam): {e}")
            print(traceback.format_exc())
            await error_handler(message.chat.id, traceback.format_exc())

    def start_game(self, customer):
        """Запуск GTA через Steam"""
        try:
            if customer.order_des["version"].lower() == "enhanced":
                os.startfile("steam://run/3240220")
            elif customer.order_des["version"].lower() == "legacy":
                os.startfile("steam://run/271590")
            else:
                print("Ошибка выбора версии GTA")
        except Exception as e:
            print(f"Ошибка запуска игры: {e}")

    async def steam_EULA(self):
        """Принятие соглашения Steam"""
        try:
            win = await wait_for_open("Steam", 15) or None
            time.sleep(1)
            if win:
                win.resizeTo(1280, 800)
                time.sleep(10)
                pyautogui.click(x=win.left + 715, y=win.top + 577)
        except Exception as e:
            print(f"Ошибка при принятии EULA: {e}")

    async def plat_guard(self, message):
        """Обработка ввода Steam Guard кода"""
        try:
            chat_id = message.chat.id
            customer = common.get_customer(chat_id)
            guard = message.text

            print(f"Получили steam guard: {guard}")
            await bot.send_message(chat_id, "Спасибо! Код получен.")

            time.sleep(1)
            pyautogui.click(x=self.win_left + 353, y=self.win_top + 320)
            time.sleep(1)
            pyautogui.click(x=self.win_left + 469, y=self.win_top + 185)
            pyautogui.write(guard, interval=0.05)
            pyautogui.press('enter')
            time.sleep(2)

            self.create_json(message)

            # if customer.type_of_soft == "Exp":
            #     if not await is_error(customer, 266, 151, 293, 161):
            #         self.start_game(customer)#здесь делаем json
            #         await self.steam_EULA()
            #         time.sleep(5)
            #         await self.rockstar_search(message)
            #     else:
            #         await bot.send_message(chat_id, "Код введен неверно, введите еще раз.")
            #         pyautogui.click(x=self.win_left + 469, y=self.win_top + 185)
            #         pyautogui.press('backspace', presses=5)
            #         customer.set_step("steam_guard")
            # else:
            #     if not await is_error(customer, 266, 151, 293, 161):
            #         await c_cliker(message)#здесь делаем json
            #     else:
            #         await bot.send_message(chat_id, "Код введен неверно, введите еще раз.")
            #         pyautogui.click(x=self.win_left + 469, y=self.win_top + 185)
            #         pyautogui.press('backspace', presses=5)
            #         customer.set_step("steam_guard")
        except Exception as e:
            print(f"Ошибка в plat_guard (Steam): {e}")
            print(traceback.format_exc())
            await error_handler(message.chat.id, traceback.format_exc())

    async def launch_prog(self, message):
        """Запуск программы Sunrise"""
        try:
            chat_id = message.chat.id
            customer = common.get_customer(chat_id)

            win_gta = await wait_for_open("Grand Theft Auto V", 200)
            self.gta = win_gta

            os.startfile(r"C:\Users\gamePC\Desktop\Sunrise.exe")
            win_sun = await wait_for_open("Sunrise", 100)

            found = False
            time.sleep(10)

            if win_gta and win_sun:
                end_time = time.time() + 85
                while time.time() < end_time:
                    r, g, b = pyautogui.pixel(2183, 1097)
                    click(2369, 148)
                    search_gray_window(found)

                win_gta.activate()
                win_sun.minimize()
                time.sleep(2.5)

                from src.Clikers.Telegram.GTACliker import gta_cliker_exp
                await gta_cliker_exp(message)
        except Exception as e:
            print(f"Ошибка в launch_prog (Steam): {e}")
            print(traceback.format_exc())
            await error_handler(message.chat.id, traceback.format_exc())

    async def plat_exit(self):
        """Выход из Steam"""
        try:
            offset_profile_x = 200
            offset_profile_y = 13
            offset_out_y = 209

            win = await wait_for_open("Steam")
            time.sleep(1)
            win.activate()

            if win:
                win_right = win.right
                win_top = win.top

                abs_x = win_right - offset_profile_x
                abs_y = win_top + offset_profile_y
                time.sleep(0.5)
                pyautogui.click(x=abs_x, y=abs_y)

                login_x = abs_x
                login_y = win.top + offset_out_y
                pyautogui.click(x=login_x, y=login_y)

                center_x = win.left + win.width // 2 + 100
                center_y = win.top + win.height // 2 + 75
                time.sleep(4)
                pyautogui.click(x=center_x, y=center_y)
                win.close()
            else:
                print("Окно не найдено")
        except Exception as e:
            print(f"Ошибка в plat_exit (Steam): {e}")

    async def close_apps(self, message):
        """Закрытие всех приложений Steam"""
        try:
            # Выход из GTA
            pyautogui.hotkey('alt', 'f4')
            if self.gta is not None:
                self.gta.activate()
                time.sleep(7)
                keyboard_press_key('enter')
                print("Вышли из GTA")

            time.sleep(5)

            # Закрытие Rockstar
            win_rock = await wait_for_open("Rockstar Games Launcher", 20) or None
            if win_rock is not None:
                win_rock.close()

            print("Закрываем Steam1")
            await self.plat_exit()

            print("Закрываем Steam2")
            win = await wait_for_open("Sign in to Steam", 10) or \
                  await wait_for_open("Войти в Steam", 10) or \
                  await wait_for_open("Steam", 10)
            if win:
                win.close()

            time.sleep(1)

            print("Закрываем cherax")
            win_cherax = await wait_for_open("Cherax Loader", 5) or \
                         await find_window_by_size(900, 600, timeout=5)
            if win_cherax is not None:
                win_cherax.activate()
                time.sleep(1)
                win_cherax.close()

            print("Цикл завершён")
            await super().close_apps(message)
        except Exception as e:
            print(f"Ошибка в close_apps (Steam): {e}")
            print(traceback.format_exc())
            await error_handler(message.chat.id, traceback.format_exc())


# Обработчик для Steam Guard
@bot.message_handler(func=lambda m: common.get_customer(m.chat.id).get_step() == "steam_guard")
async def handle_steam_guard(message):
    """Обработчик ввода Steam Guard"""
    try:
        chat_id = message.chat.id
        customer = common.get_customer(chat_id)

        if customer.clicker and isinstance(customer.clicker, SteamClicker):
            await customer.clicker.plat_guard(message)
    except Exception as e:
        print(f"Ошибка в handle_steam_guard: {e}")
        await error_handler(message.chat.id, traceback.format_exc())