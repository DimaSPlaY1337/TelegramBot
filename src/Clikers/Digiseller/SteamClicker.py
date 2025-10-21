import asyncio
import time

from src.Handlers.Digiseller.IO_utils import send_message, get_messages, wait_for_message
from src.common import *
from src.Clikers.Digiseller.PlatformClicker import PlatformClicker
from src.Clikers.Digiseller.input_utils import *
from src.Clikers.Digiseller.Cherax_cliker import c_cliker

class SteamClicker(PlatformClicker):

    def __init__(self):
        super().__init__()

    async def plat_clicker(self, token, dialog_id, message_text, customer):
        await super().plat_clicker(token, dialog_id, message_text, customer)

        os.startfile("C:\\Program Files\\Rockstar Games\\Launcher\\LauncherPatcher.exe")
        # win_rock = await wait_for_open("Rockstar Games - Sign In")
        time.sleep(10)
        # if win_rock:
        #     win_rock.minimize()

        os.startfile("C:\\Program Files (x86)\\Steam\\Steam.exe")

        switch_to_english()

        offset_plus_x = 445  # смещение по X от левого верхнего угла окна
        offset_plus_y = 220  # смещение по Y от левого верхнего угла окна

        offset_login_x = 145  # смещение по X от левого верхнего угла окна
        offset_login_y = 150  # смещение по Y от левого верхнего угла окна

        offset_password_x = offset_login_x  # смещение по X от левого верхнего угла окна
        offset_password_y = offset_plus_y  # смещение по Y от левого верхнего угла окна

        offset_enter_x = 325  # смещение по X от левого верхнего угла окна
        offset_enter_y = 300  # смещение по Y от левого верхнего угла окна

        time.sleep(0.5)
        win = await wait_for_open("Sign in to Steam", 20) or await wait_for_open("Войти в Steam", 20)

        if win:
            win.resizeTo(705, 440)
            time.sleep(0.2)
            win.activate()
            customer.clicker.win_left = win.left
            customer.clicker.win_top = win.top

            abs_x = win.left + offset_plus_x
            abs_y = win.top + offset_plus_y

            time.sleep(0.5)  # время на переключение окна
            pyautogui.click(x=abs_x, y=abs_y)
            # time.sleep(1)

            login_x = win.left + offset_login_x
            login_y = win.top + offset_login_y

            win.activate()
            time.sleep(0.2)
            pyautogui.click(x=login_x, y=login_y)
            pyautogui.click(x=login_x, y=login_y)
            write_data(login_x, login_y, customer.data_for_reg["login"])

            pass_x = win.left + offset_password_x
            pass_y = win.top + offset_password_y

            win.activate()
            time.sleep(0.2)
            pyautogui.click(x=pass_x, y=pass_y)
            pyautogui.click(x=pass_x, y=pass_y)
            write_data(pass_x, pass_y, customer.data_for_reg["password"])

            pass_cb_x = win.left + offset_enter_x
            pass_cb_y = win.top + offset_enter_y

            pyautogui.click(x=pass_cb_x, y=pass_cb_y)

            add_kode_x = win.left + 352
            add_kode_y = win.top + 320

            pyautogui.click(x=add_kode_x, y=add_kode_y)

            if not await is_error(customer,51, 339, 121, 352):
                time.sleep(5)

                win = await wait_for_open("Sign in to Steam", 5) or await wait_for_open("Войти в Steam", 5)
                if win:
                    customer.clicker.win_top = win.top
                    customer.clicker.win_left = win.left
                    customer.user_step = "steam_guard"
                    await send_message(token, dialog_id, "Введите код Steam Guard (или другой нужный код):")

                    guard = await wait_for_message(token, dialog_id)
                    await self.plat_guard(token, dialog_id, guard, customer)
                else:
                    if type_of_soft == "Exp":
                        self.start_game(customer)
                        await self.steam_EULA()
                        time.sleep(5)
                        await self.rockstar_search(token, dialog_id, message_text, customer)
                        print("Окно steam guard не найдено")
                    else:
                        await c_cliker(token, dialog_id, message_text, customer)

            else:
                win.close()
                await self.change_pass_and_login(token, dialog_id, message_text, customer)
        else:
            print("Окно не найдено")

    def start_game(self, customer):
        if customer.order_des["version"] == "Enhanced":
            os.startfile("steam://run/3240220")
        elif customer.order_des["version"] == "Legacy":
            os.startfile("steam://run/271590")
        else:
            print("Ошибка выбора версии GTA")

    async def steam_EULA(self):
        win = await wait_for_open("Steam", 15) or None
        if win:
            win.resizeTo(1280, 800)
            time.sleep(10)
            pyautogui.click(x=win.left + 715, y=win.top + 577)

    # @bot.message_handler(func=lambda m: user_step.get(m.chat.id, {}).get("step") == "steam_guard")
    async def plat_guard(self, token, dialog_id, message_text, customer):
        guard = message_text  # Здесь — то, что ввел пользователь!
        print(f"Получили steam guard: {guard}")
        await send_message(token, dialog_id, "Спасибо! Код получен.")

        time.sleep(1)
        pyautogui.click(x=self.win_left + 353, y=self.win_top + 320)
        time.sleep(1)

        pyautogui.click(x=self.win_left + 469, y=self.win_top + 185)
        pyautogui.write(guard, interval=0.05)
        pyautogui.press('enter')

        time.sleep(2)
        if customer.type_of_soft == "Exp":
            if not await is_error(customer,266, 151, 293, 161):
                self.start_game(customer)
                await self.steam_EULA()
                time.sleep(5)
                await self.rockstar_search(token, dialog_id, message_text, customer)
            else:
                await send_message(token, dialog_id, "Код введен неверно, введите еще раз.")
                pyautogui.click(x=self.win_left + 469, y=self.win_top + 185)
                pyautogui.press('backspace', 5)

                guard = await wait_for_message(token, dialog_id)
                await self.plat_guard(token, dialog_id, guard, customer)
        else:
            if not await is_error(customer,266, 151, 293, 161):
                await c_cliker(token, dialog_id, message_text, customer)
            else:
                await send_message(token, dialog_id, "Код введен неверно, введите еще раз.")
                pyautogui.click(x=self.win_left + 469, y=self.win_top + 185)
                pyautogui.press('backspace', 5)

                guard = await wait_for_message(token, dialog_id)
                await self.plat_guard(token, dialog_id, guard, customer)

    async def launch_prog(self, token, dialog_id, message_text, customer):
        win_gta = await wait_for_open("Grand Theft Auto V", 200)
        gta = win_gta

        win_sun = None
        if customer.order_des["version"] == "enhanced":
            os.startfile(r"C:\Users\gamePC\Desktop\Enhanced.exe")
        elif customer.order_des["version"] == "legacy":
            os.startfile(r"C:\Users\gamePC\Desktop\Legacy.exe")
        else:
            print("Ошибка выбора версии Sunrise")

        win_sun = await wait_for_open("Sunrise", 100)

        found = False
        time.sleep(10)
        if win_gta and win_sun:
            end_time = time.time() + 85
            while time.time() < end_time:
                r, g, b = pyautogui.pixel(2183, 1097)
                if is_gray(r, g, b) and found == False:
                    keyboard_press_key('enter')
                    print("Нашли серое окно GTA")
                    found = True
                win_gta.activate()
                win_sun.minimize()
                time.sleep(2.5)
            from src.Clikers.Digiseller.GTACliker import gta_cliker_exp
            await gta_cliker_exp(token, dialog_id, message_text, customer)

    async def plat_exit(self):
        offset_profile_x = 200  # смещение по X от левого верхнего угла окна
        offset_profile_y = 13  # смещение по Y от левого верхнего угла окна

        offset_out_x = 944  # смещение по X от левого верхнего угла окна
        offset_out_y = 209  # смещение по Y от левого верхнего угла окна

        win = await wait_for_open("Steam")
        time.sleep(1)
        win.activate()
        if win:
            win_right = win.right
            win_top = win.top

            abs_x = win_right - offset_profile_x
            abs_y = win_top + offset_profile_y

            time.sleep(0.5)  # время на переключение окна
            pyautogui.click(x=abs_x, y=abs_y)

            login_x = abs_x
            login_y = win.top + offset_out_y

            pyautogui.click(x=login_x, y=login_y)

            center_x = win.left + win.width // 2 + 100
            center_y = win.top + win.height // 2 + 75

            time.sleep(0.5)
            pyautogui.click(x=center_x, y=center_y)

            win.close()
        else:
            print("Окно не найдено")

    async def close_apps(self, token, dialog_id, message_text, customer):
        # выход из гта
        pyautogui.hotkey('alt', 'f4')
        if self.gta is not None:
            self.gta.activate()
        time.sleep(7)
        keyboard_press_key('enter')
        print("Вышли из GTA")

        time.sleep(5)

        win_rock = await wait_for_open("Rockstar Games Launcher", 20) or None
        if win_rock is not None:
            win_rock.close()

        print("Закрываем Steam1")
        await self.plat_exit()

        print("Закрываем Steam2")
        win = await wait_for_open("Sign in to Steam", 20) or await wait_for_open("Войти в Steam", 20) or await wait_for_open("Steam", 20)
        if win:
            win.close()

        time.sleep(1)

        print("Закрываем cherax")
        win_cherax = await wait_for_open("Cherax Loader", 5) or await find_window_by_size(900, 600, timeout=5)
        if win_cherax is not None:
            win_cherax.activate()
            time.sleep(1)
            win_cherax.close()

        print("Цикл завершён")
        await super().close_apps(token, dialog_id, message_text, customer)