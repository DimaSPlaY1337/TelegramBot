import time

from src.Handlers.Digiseller.IO_utils import send_message, wait_for_message
from src.common import *
from src.Clikers.Digiseller.PlatformClicker import PlatformClicker
from src.Clikers.Digiseller.input_utils import *
from src.Clikers.Digiseller.Cherax_cliker import c_cliker

class RockstarClicker(PlatformClicker):

    def __init__(self):
        super().__init__()

    async def plat_clicker(self, token, dialog_id, message_text, customer):
        await super().plat_clicker(token, dialog_id, message_text, customer)

        os.startfile("C:\\Program Files\\Rockstar Games\\Launcher\\LauncherPatcher.exe")
        switch_to_english()

        offset_password_x = 250  # смещение по X от левого верхнего угла окна
        offset_password_y = 420  # смещение по Y от левого верхнего угла окна

        offset_enter_x = 520  # смещение по X от левого верхнего угла окна
        offset_enter_y = 520  # смещение по Y от левого верхнего угла окна

        time.sleep(0.5)
        win = await wait_for_open("Rockstar Games - Sign In", 100)
        if win:
            win.resizeTo(700, 800)
            time.sleep(0.3)
            win.activate()
            time.sleep(0.2)
            customer.clicker.win_left = win.left
            customer.clicker.win_top = win.top

            login_x = win.left + 250
            login_y = win.top + 350

            time.sleep(3)
            write_data(login_x, login_y, customer.data_for_reg["login"])

            pass_x = win.left + offset_password_x
            pass_y = win.top + offset_password_y

            write_data(pass_x, pass_y, customer.data_for_reg["password"])

            abs_x = win.left + offset_enter_x
            abs_y = win.top + offset_enter_y

            pyautogui.click(x=abs_x, y=abs_y)

            time.sleep(4)
            if (not await is_error(customer,101, 186, 141, 204)
                    and not await is_error(customer,123, 351, 134, 359)):
                time.sleep(5)

                win = await wait_for_open("Rockstar Games - Sign In", 10) or None
                if win:
                    customer.clicker.win_top = win.top
                    customer.clicker.win_left = win.left
                    customer.user_step = "rockstar_guard"
                    await send_message(token, dialog_id, "Введите код RockStar Guard (или другой нужный код):")

                    guard = await wait_for_message(token, dialog_id)
                    await self.plat_guard(token, dialog_id, guard, customer)
                else:
                    if customer.type_of_soft == "Exp":
                        await self.launch_prog(token, dialog_id, message_text, customer)
                    else:
                        await c_cliker(token, dialog_id, message_text, customer)
            else:
                win.close()
                await self.change_pass_and_login(token, dialog_id, message_text, customer)
        else:
            print("Окно не найдено")

    # @bot.message_handler(func=lambda m: common.user_step.get(m.chat.id, {}).get("step") == "rockstar_guard")
    async def plat_guard(self, token, dialog_id, message_text, customer):
        guard = message_text  # Здесь — то, что ввел пользователь!
        print(f"Получили steam guard: {guard}")
        await send_message(token, dialog_id, "Спасибо! Код получен.")

        pyautogui.click(x=customer.clicker.win_left + 318, y=customer.clicker.win_top + 451)
        pyautogui.write(guard, interval=0.05)
        pyautogui.click(x=customer.clicker.win_left + 538, y=customer.clicker.win_top + 563)

        #2-step verification
        pyautogui.click(x=customer.clicker.win_left + 522, y=customer.clicker.win_top + 517)

        if customer.type_of_soft == "Exp":
            if not await is_error(customer,430, 650, 440, 660):  # узнать коор ошибки при вводе кода
                await self.launch_prog(token, dialog_id, message_text, customer)
            else:
                await send_message(token, dialog_id, "Код введен неверно, введите еще раз.")

                guard = await wait_for_message(token, dialog_id)
                await self.plat_guard(token, dialog_id, guard, customer)
        else:
            if not await is_error(customer, 430, 650, 440, 660):  # узнать коор ошибки при вводе кода
                await c_cliker(token, dialog_id, message_text, customer)
            else:
                await send_message(token, dialog_id, "Код введен неверно, введите еще раз.")

                guard = await wait_for_message(token, dialog_id)
                await self.plat_guard(token, dialog_id, guard, customer)

    async def launch_prog(self, token, dialog_id, message_text, customer):
        # протокола нету как у steam
        if customer.order_des["version"] == "Enhanced":
            os.startfile(r"C:\Users\gamePC\Desktop\GTA`s\GTA_RE.lnk")
        elif customer.order_des["version"] == "Legacy":
            os.startfile(r"C:\Users\gamePC\Desktop\GTA`s\GTA_RL.lnk")
        else:
            print("Ошибка выбора версии GTA")

        win_gta = await wait_for_open("Grand Theft Auto V", 200)
        gta = win_gta

        win_rock = await wait_for_open("Rockstar Games Launcher", 100)

        if customer.order_des["version"] == "Enhanced":
            os.startfile(r"C:\Users\gamePC\Desktop\Enhanced.exe")
        elif customer.order_des["version"] == "Legacy":
            os.startfile(r"C:\Users\gamePC\Desktop\Legacy.exe")
        else:
            print("Ошибка выбора версии Sunrise")

        win_sun = await wait_for_open("Sunrise", 40)

        found = False
        time.sleep(10)
        if win_gta and win_sun:
            end_time = time.time() + 90
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
        offset_profile_x = 1031  # смещение по X от левого верхнего угла окна
        offset_profile_y = 67  # смещение по Y от левого верхнего угла окна

        offset_out_x = 969  # смещение по X от левого верхнего угла окна
        offset_out_y = 336  # смещение по Y от левого верхнего угла окна

        # windows = gw.getAllWindows()
        # print([w.title for w in windows])
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

    async def close_apps(self, token):
        # выход из гта
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

        await self.close_sunrise()
        print("Цикл завершён")
        await super().close_apps(token)