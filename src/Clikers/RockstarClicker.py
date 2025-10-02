import src.common as common
from src.common import *
from src.Clikers.PlatformClicker import PlatformClicker
from src.Clikers.input_utils import *
from src.Clikers.Cherax_cliker import c_cliker

class RockstarClicker(PlatformClicker):

    def __init__(self):
        super().__init__()

    async def plat_clicker(self, message):
        global win_left, win_top
        await super().plat_clicker(message)

        os.startfile("C:\\Program Files\\Rockstar Games\\Launcher\\LauncherPatcher.exe")
        switch_to_english()

        win_be = None
        if not await wait_for_open("C:\\Users\\gamePC\\Desktop\\beSkip.exe", 3):
            os.startfile(r"C:\Users\gamePC\Desktop\beSkip.exe", 'runas')
            win_be = await wait_for_open("C:\\Users\\gamePC\\Desktop\\beSkip.exe")
        else:
            win_be = await wait_for_open("C:\\Users\\gamePC\\Desktop\\beSkip.exe")

        global win_left, win_top

        offset_login_x = 250  # смещение по X от левого верхнего угла окна
        offset_login_y = 350  # смещение по Y от левого верхнего угла окна

        offset_password_x = 250  # смещение по X от левого верхнего угла окна
        offset_password_y = 420  # смещение по Y от левого верхнего угла окна

        offset_enter_x = 520  # смещение по X от левого верхнего угла окна
        offset_enter_y = 520  # смещение по Y от левого верхнего угла окна

        time.sleep(0.5)
        win = await wait_for_open("Rockstar Games - Sign In")
        if win:
            win.resizeTo(700, 800)
            time.sleep(0.3)
            win.activate()
            time.sleep(0.2)
            win_left = win.left
            win_top = win.top

            login_x = win.left + offset_login_x
            login_y = win.top + offset_login_y

            write_data(login_x, login_y, common.data_for_reg[message.chat.id]["login"])

            pass_x = win.left + offset_password_x
            pass_y = win.top + offset_password_y

            write_data(pass_x, pass_y, common.data_for_reg[message.chat.id]["password"])

            abs_x = win.left + offset_enter_x
            abs_y = win.top + offset_enter_y

            pyautogui.click(x=abs_x, y=abs_y)

            time.sleep(4)
            if (not await is_error(101, 186, 141, 204)
                    and not await is_error(123, 351, 134, 359)):
                time.sleep(5)

                win = await wait_for_open("Rockstar Games - Sign In", 5) or None
                if win:
                    win_top = win.top
                    win_left = win.left
                    common.user_step[message.chat.id] = {"step": "rockstar_guard"}
                    await bot.send_message(message.chat.id, "Введите код RockStar Guard (или другой нужный код):")
                else:
                    if common.type_of_soft == "Exp":
                        await self.launch_prog(message)
                    else:
                        await c_cliker(message)
            else:
                win.close()
                await self.change_pass_and_login(message)
                await bot.send_message(message.chat.id, "Введите еще раз")
        else:
            print("Окно не найдено")

    @bot.message_handler(func=lambda m: common.user_step.get(m.chat.id, {}).get("step") == "rockstar_guard")
    async def plat_guard(self, message):
        guard = message.text  # Здесь — то, что ввел пользователь!
        print(f"Получили steam guard: {guard}")

        await bot.send_message(message.chat.id, "Спасибо! Код получен.")
        pyautogui.click(x=win_left + 318, y=win_top + 451)
        pyautogui.write(guard, interval=0.05)
        pyautogui.click(x=win_left + 538, y=win_top + 563)

        if common.type_of_soft == "Exp":
            if not await is_error(430, 650, 440, 660):  # узнать коор ошибки при вводе кода
                await self.launch_prog(message)
            else:
                await bot.send_message(message.chat.id, "Код введен неверно, введите еще раз.")
        else:
            if not await is_error(430, 650, 440, 660):  # узнать коор ошибки при вводе кода
                await c_cliker(message)
            else:
                await bot.send_message(message.chat.id, "Код введен неверно, введите еще раз.")

    async def launch_prog(self, message):
        # протокола нету как у steam
        if common.order_des[message.chat.id]["version"] == "Enhanced":
            os.startfile(r"C:\Users\gamePC\Desktop\GTA`s\GTA_RE.lnk")
        elif common.order_des[message.chat.id]["version"] == "Legacy":
            os.startfile(r"C:\Users\gamePC\Desktop\GTA`s\GTA_RL.lnk")
        else:
            print("Ошибка выбора версии GTA")

        win_gta = await wait_for_open("Grand Theft Auto V", 200)
        gta = win_gta

        win_rock = await wait_for_open("Rockstar Games Launcher", 100)

        if common.order_des[message.chat.id]["version"] == "Enhanced":
            os.startfile(r"C:\Users\gamePC\Desktop\Enhanced.exe")
        elif common.order_des[message.chat.id]["version"] == "Legacy":
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
            from src.Clikers.GTACliker import gta_cliker_exp
            await gta_cliker_exp(message)

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

    async def close_apps(self):
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