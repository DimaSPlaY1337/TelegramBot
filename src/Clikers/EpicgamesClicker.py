from src.Clikers.PlatformClicker import PlatformClicker
from src.Clikers.input_utils import *
import src.common as common
from src.common import *

class EpicgamesClicker(PlatformClicker):

    def __init__(self):
        super().__init__()

    async def plat_clicker(self, message):
        global win_left, win_top
        await super().plat_clicker(message)

        os.startfile("C:\\Program Files\\Rockstar Games\\Launcher\\LauncherPatcher.exe")
        win = await wait_for_open("Rockstar Games - Sign In")
        if win:
            print("Rockstar в Epic открылся")
        else:
            print("Rockstar в Epic не открылся")

        os.startfile("C:\\Program Files (x86)\\Epic Games\\Launcher\\Portal\\Binaries\\Win32\\EpicGamesLauncher.exe")
        switch_to_english()

        offset_login_x = 584  # смещение по X от левого верхнего угла окна
        offset_login_y = 584  # смещение по Y от левого верхнего угла окна

        offset_login_cb_x = 647  # смещение по X от левого верхнего угла окна
        offset_login_cb_y = 647  # смещение по Y от левого верхнего угла окна

        offset_password_x = 665  # смещение по X от левого верхнего угла окна
        offset_password_y = 731  # смещение по Y от левого верхнего угла окна

        offset_password_cb_x = 643  # смещение по X от левого верхнего угла окна
        offset_password_cb_y = 847  # смещение по Y от левого верхнего угла окна

        # windows = gw.getAllWindows()
        # print([w.title for w in windows])

        win = await wait_for_open("Epic Games Launcher")
        if win:
            win.resizeTo(1324, 1400)
            win_left = win.left
            win_top = win.top

            login_x = win.left + offset_login_x
            login_y = win.top + offset_login_y

            login_cb_x = win.left + offset_login_cb_x
            login_cb_y = win.top + offset_login_cb_y

            guard_x = win.left + 318
            guard_y = win.top + 451

            guard_write_x = win_left + 560
            guard_write_y = win_top + 748

            time.sleep(5)
            write_data(login_x, login_y, common.data_for_reg[message.chat.id]["login"])

            pyautogui.click(x=login_cb_x, y=login_cb_y)
            pyautogui.click(x=login_cb_x, y=login_cb_y)

            if not await is_error(444, 623, 539, 632):

                pass_x = win.left + offset_password_x
                pass_y = win.top + offset_password_y

                pyautogui.click(x=pass_x, y=pass_y)

                write_data(pass_x, pass_y, common.data_for_reg[message.chat.id]["password"])

                pass_cb_x = win.left + offset_password_cb_x
                pass_cb_y = win.top + offset_password_cb_y

                pyautogui.click(x=pass_cb_x, y=pass_cb_y)

                if not await is_error(434, 740, 508, 751):
                    time.sleep(3)
                    common.user_step[message.chat.id] = {"step": "epic_guard"}
                    await bot.send_message(message.chat.id, "Введите код RockStar Guard (или другой нужный код):")
                else:
                    win.close()
                    await self.change_pass_and_login(message)
            else:
                win.close()
                await self.change_pass_and_login(message)
        else:
            print("Окно не найдено")

    @bot.message_handler(func=lambda m: common.user_step.get(m.chat.id, {}).get("step") == "epic_guard")
    async def plat_guard(self, message):
        guard = message.text  # Здесь — то, что ввел пользователь!
        print(f"Получили steam guard: {guard}")

        await bot.send_message(message.chat.id, "Спасибо! Код получен.")
        pyautogui.click(x=win_left + 560, y=win_top + 748)
        pyautogui.write(guard, interval=0.05)
        pyautogui.press('enter')

        time.sleep(3)
        if not await is_error(430, 650, 477, 700):
            await self.launch_prog(message)
        else:
            await bot.send_message(message.chat.id, "Код введен неверно, введите еще раз.")

    async def launch_prog(self, message):
        if common.order_des[message.chat.id]["version"] == "Enhanced":
            os.startfile(r"C:\Users\gamePC\Desktop\GTA`s\GTA_EE.url")
        elif common.order_des[message.chat.id]["version"] == "Legacy":
            os.startfile(r"C:\Users\gamePC\Desktop\GTA`s\GTA_EL.url")
        else:
            print("Ошибка выбора версии GTA")

        win_gta = await wait_for_open("Grand Theft Auto V", 200)
        gta = win_gta

        win_rock = await wait_for_open("Rockstar Games", 20)
        if win_rock:
            rock_win = win_rock
            common.user_step[message.chat.id] = {"step": "rock_steam_guard"}
            await bot.send_message(message.chat.id, "Введите код RockStar Guard (или другой нужный код):")
        common.app_list.append(win_rock)

        if common.order_des[message.chat.id]["version"] == "Enhanced":
            os.startfile(r"C:\Users\gamePC\Desktop\Enhanced.exe")
        elif common.order_des[message.chat.id]["version"] == "Legacy":
            os.startfile(r"C:\Users\gamePC\Desktop\Legacy.exe")
        else:
            print("Ошибка выбора версии Sunrise")

        win_sun = await wait_for_open("Sunrise", 40)
        # app_list.append(win_sun)

        time.sleep(10)
        if win_gta and win_sun:
            end_time = time.time() + 90
            while time.time() < end_time:
                # keyboard_press_key('enter')
                win_gta.activate()
                win_sun.minimize()
                time.sleep(2.5)
            from src.Clikers.GTACliker import gta_cliker_exp
            await gta_cliker_exp(message)

    async def plat_exit(self):
        offset_profile_x = 1257  # смещение по X от левого верхнего угла окна
        offset_profile_y = 78  # смещение по Y от левого верхнего угла окна

        offset_out_x = 952  # смещение по X от левого верхнего угла окна
        offset_out_y = 689  # смещение по Y от левого верхнего угла окна

        offset_accept_x = 741  # смещение по X от левого верхнего угла окна
        offset_accept_y = 774  # смещение по Y от левого верхнего угла окна

        # windows = gw.getAllWindows()
        # print([w.title for w in windows])
        # Программа
        # запуска
        # Epic
        # Games
        win = await wait_for_open("Epic Games Launcher")
        win.activate()
        if win:
            win.resizeTo(1324, 1400)
            win_left = win.left
            win_top = win.top

            abs_x = win_left + offset_profile_x

            abs_y = win_top + offset_profile_y

            time.sleep(1)  # время на переключение окна
            pyautogui.click(x=abs_x, y=abs_y)

            login_x = win_left + offset_out_x
            login_y = win.top + offset_out_y

            time.sleep(1)
            pyautogui.click(x=login_x, y=login_y)

            win.close()
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