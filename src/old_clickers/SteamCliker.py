# import os
# from src.Clikers.input_utils import *
#
# from src.Clikers.Cherax_cliker import c_cliker
# from src.Handlers import globals
#
# from src.common import bot
#
# win_left = 0
# win_top = 0
#
# gta = None
#
# sign_in_rock_button = None
#
# async def steam_EULA():
#     win = await wait_for_open("Steam", 15) or None
#     if win:
#         win.resizeTo(1280, 800)
#         time.sleep(10)
#         win_left = win.left
#         win_top = win.top
#
#         pyautogui.click(x=win_left + 715, y=win_top + 577)
#
# def start_game(message):
#     if globals.order_des[message.chat.id]["version"] == "Enhanced":
#         os.startfile("steam://run/3240220")
#
#     elif globals.order_des[message.chat.id]["version"] == "Legacy":
#         os.startfile("steam://run/271590")
#
#     else:
#         print("Ошибка выбора версии GTA")
#
# @bot.message_handler(func=lambda m: globals.user_step.get(m.chat.id, {}).get("step") == "cliker_steam")
# async def steam_cliker(message):
#     global win_left, win_top
#
#     if globals.order_des[message.chat.id]["amount"].isdigit():
#         if int(globals.order_des[message.chat.id]["amount"]) >= 75000000:
#             globals.type_of_soft = "Exp"
#         else:
#             globals.type_of_soft = "Free"
#     else:
#         globals.type_of_soft = "Free"
#
#     os.startfile("C:\\Program Files\\Rockstar Games\\Launcher\\LauncherPatcher.exe")
#
#     time.sleep(7)
#
#     win_be = None
#     if not await wait_for_open("C:\\Users\\gamePC\\Desktop\\beSkip.exe", 3):
#         os.startfile(r"C:\Users\gamePC\Desktop\beSkip.exe", 'runas')
#         win_be = await wait_for_open("C:\\Users\\gamePC\\Desktop\\beSkip.exe")
#     else:
#         win_be = await wait_for_open("C:\\Users\\gamePC\\Desktop\\beSkip.exe")
#
#     os.startfile("C:\\Program Files (x86)\\Steam\\Steam.exe")
#     switch_to_english()
#
#     offset_plus_x = 445  # смещение по X от левого верхнего угла окна
#     offset_plus_y = 220  # смещение по Y от левого верхнего угла окна
#
#     offset_login_x = 145  # смещение по X от левого верхнего угла окна
#     offset_login_y = 150  # смещение по Y от левого верхнего угла окна
#
#     offset_password_x = offset_login_x  # смещение по X от левого верхнего угла окна
#     offset_password_y = offset_plus_y  # смещение по Y от левого верхнего угла окна
#
#     offset_enter_x = 325  # смещение по X от левого верхнего угла окна
#     offset_enter_y = 300  # смещение по Y от левого верхнего угла окна
#
#     time.sleep(0.5)
#     win = await wait_for_open("Sign in to Steam", 100) or await wait_for_open("Войти в Steam", 100)
#     if win:
#         win.resizeTo(705, 440)
#         time.sleep(0.2)
#         win.activate()
#         win_left = win.left
#         win_top = win.top
#
#         abs_x = win_left + offset_plus_x
#         abs_y = win_top + offset_plus_y
#
#         time.sleep(0.5)  # время на переключение окна
#         pyautogui.click(x=abs_x, y=abs_y)
#         # time.sleep(1)
#
#         login_x = win_left + offset_login_x
#         login_y = win.top + offset_login_y
#
#
#         win.activate()
#         time.sleep(0.2)
#         pyautogui.click(x=login_x, y=login_y)
#         pyautogui.click(x=login_x, y=login_y)
#         write_data(login_x, login_y, globals.data_for_reg[message.chat.id]["login"])
#
#         pass_x = win_left + offset_password_x
#         pass_y = win.top + offset_password_y
#
#
#         win.activate()
#         time.sleep(0.2)
#         pyautogui.click(x=pass_x, y=pass_y)
#         pyautogui.click(x=pass_x, y=pass_y)
#         write_data(pass_x, pass_y, globals.data_for_reg[message.chat.id]["password"])
#
#         pass_cb_x = win_left + offset_enter_x
#         pass_cb_y = win.top + offset_enter_y
#
#         pyautogui.click(x=pass_cb_x, y=pass_cb_y)
#
#         add_kode_x = win_left + 352
#         add_kode_y = win_top + 320
#
#         pyautogui.click(x=add_kode_x, y=add_kode_y)
#
#         if not await is_error(51, 339, 121, 352):
#             time.sleep(10)
#
#             win = await wait_for_open("Sign in to Steam", 5) or None
#             if win:
#                 win_top = win.top
#                 win_left = win.left
#                 globals.user_step[message.chat.id] = {"step": "steam_guard"}
#                 await bot.send_message(message.chat.id, "Введите код Steam Guard (или другой нужный код):")
#             else:
#                 if globals.type_of_soft == "Exp":
#                     start_game(message)
#                     await steam_EULA()
#                     time.sleep(5)
#                     await rockstar_search(message)
#                     print("Окно steam guard не найдено")
#                 else:
#                     await c_cliker(message)
#
#         else:
#             win.close()
#             await change_pass_and_login(message)
#     else:
#         print("Окно не найдено")
#
# @bot.message_handler(func=lambda m: globals.user_step.get(m.chat.id, {}).get("step") == "steam_guard")
# async def steam_guard(message):
#     global win_left, win_top
#
#     guard = message.text  # Здесь — то, что ввел пользователь!
#     print(f"Получили steam guard: {guard}")
#     await bot.send_message(message.chat.id, "Спасибо! Код получен.")
#
#     time.sleep(1)
#     pyautogui.click(x=win_left + 353, y=win_top + 320)
#     time.sleep(1)
#
#     pyautogui.click(x=win_left + 469, y=win_top + 185)
#     pyautogui.write(guard, interval=0.05)
#     pyautogui.press('enter')
#
#     time.sleep(2)
#     if globals.type_of_soft == "Exp":
#         if not await is_error(266, 151, 293, 161):
#             start_game(message)
#             await steam_EULA()
#             time.sleep(5)
#             await rockstar_search(message)
#         else:
#             await bot.send_message(message.chat.id, "Код введен неверно, введите еще раз.")
#             pyautogui.click(x=win_left + 469, y=win_top + 185)
#             pyautogui.press('backspace', 5)
#     else:
#         if not await is_error(266, 151, 293, 161):
#                 await c_cliker(message)
#         else:
#             await bot.send_message(message.chat.id, "Код введен неверно, введите еще раз.")
#             pyautogui.click(x=win_left + 469, y=win_top + 185)
#             pyautogui.press('backspace', 5)
#
# @bot.message_handler(func=lambda m: globals.user_step.get(m.chat.id, {}).get("step") == "rock_steam_guard")
# async def rockstar_cliker(message):
#     global win_left, win_top, sign_in_rock_button
#
#     rock_guard = message.text
#     print(f"Получили rock guard: {rock_guard}")
#     await bot.send_message(message.chat.id, "Спасибо! Код получен.")
#
#     pyautogui.click(x=win_left + 233, y=win_top + 475)
#     time.sleep(0.2)
#     pyautogui.write(rock_guard, interval=0.05)
#     pyautogui.click(x=win_left + 527, y=sign_in_rock_button)
#
#     time.sleep(6)
#     if await is_error(368, 508, 388, 511):  # узнать коор ошибки при вводе кода
#         await bot.send_message(message.chat.id, "Код введен неверно, введите еще раз.")
#         sign_in_rock_button = win_top + 622
#     else:
#         await rockstar_acceptance(message)
#
# async def rockstar_search(message):
#     global win_left, win_top, sign_in_rock_button
#
#     win_rock = await wait_for_open("Rockstar Games - Sign In", 100)
#     if win_rock:
#         win_left = win_rock.left
#         win_top = win_rock.top
#         sign_in_rock_button = win_top + 601
#
#         globals.user_step[message.chat.id] = {"step": "rock_steam_guard"}
#         await bot.send_message(message.chat.id, "Введите код RockStar Guard (или другой нужный код):")
#     else:
#         await launch_prog(message)
#
# async def rockstar_acceptance(message):
#     global win_left, win_top
#
#     time.sleep(12)
#     win_rock = await wait_for_open("Rockstar Games Launcher", 100)
#     if win_rock:
#         win_rock.resizeTo(1024, 600)
#         time.sleep(0.5)
#         win_rock.activate()
#         time.sleep(0.5)
#
#         win_left = win_rock.left
#         win_top = win_rock.top
#
#         pyautogui.click(x=win_left + 831, y=win_top + 412)#узнать координаты
#
#     time.sleep(5)
#     await launch_prog(message)
#
# async def launch_prog(message):
#     global gta
#
#     win_gta = await wait_for_open("Grand Theft Auto V", 200)
#     gta = win_gta
#
#     win_sun = None
#     if globals.order_des[message.chat.id]["version"] == "Enhanced":
#         os.startfile(r"C:\Users\gamePC\Desktop\Enhanced.exe")
#     elif globals.order_des[message.chat.id]["version"] == "Legacy":
#         os.startfile(r"C:\Users\gamePC\Desktop\Legacy.exe")
#     else:
#         print("Ошибка выбора версии Sunrise")
#
#     win_sun = await wait_for_open("Sunrise", 100)
#
#     found = False
#     time.sleep(10)
#     if win_gta and win_sun:
#         end_time = time.time() + 85
#         while time.time() < end_time:
#             r,g,b = pyautogui.pixel(2183, 1097)
#             if is_gray(r,g,b) and found == False:
#                 keyboard_press_key('enter')
#                 print("Нашли серое окно GTA")
#                 found = True
#             win_gta.activate()
#             win_sun.minimize()
#             time.sleep(2.5)
#         from src.Clikers.GTACliker import gta_cliker_exp
#         await gta_cliker_exp(message)
#
# async def steam_exit():
#     global win_left, win_top
#
#     offset_profile_x = 200  # смещение по X от левого верхнего угла окна
#     offset_profile_y = 13  # смещение по Y от левого верхнего угла окна
#
#     offset_out_x = 944  # смещение по X от левого верхнего угла окна
#     offset_out_y = 209  # смещение по Y от левого верхнего угла окна
#
#     win = await wait_for_open("Steam")
#     time.sleep(1)
#     win.activate()
#     if win:
#         win_right = win.right
#         win_top = win.top
#
#         abs_x = win_right - offset_profile_x
#         abs_y = win_top + offset_profile_y
#
#         time.sleep(0.5)  # время на переключение окна
#         pyautogui.click(x=abs_x, y=abs_y)
#
#         login_x = abs_x
#         login_y = win.top + offset_out_y
#
#         pyautogui.click(x=login_x, y=login_y)
#
#         center_x = win.left + win.width // 2 + 100
#         center_y = win.top + win.height // 2 + 75
#
#         time.sleep(0.5)
#         pyautogui.click(x=center_x, y=center_y)
#
#         win.close()
#     else:
#         print("Окно не найдено")
#
# async def close_apps():
#     # выход из гта
#     pyautogui.hotkey('alt', 'f4')
#     if gta is not None:
#         gta.activate()
#     time.sleep(7)
#     keyboard_press_key('enter')
#     print("Вышли из GTA")
#
#     time.sleep(5)
#
#     win_rock = await wait_for_open("Rockstar Games Launcher", 20) or None
#     if win_rock is not None:
#         win_rock.close()
#
#     print("Закрываем Steam1")
#     await steam_exit()
#
#     print("Закрываем Steam2")
#     win = await wait_for_open("Sign in to Steam", 100) or await wait_for_open("Войти в Steam", 100)
#     if win:
#         win.close()
#
#     time.sleep(1)
#
#     await close_sunrise()
#     print("Цикл завершён")
#
# async def close_sunrise():
#     win = await wait_for_open("Sunrise", 40)
#     time.sleep(1)
#     win.activate()
#     pyautogui.hotkey('alt', 'f4')
#     time.sleep(0.3)
#     pyautogui.hotkey('alt', 'f4')
#     time.sleep(0.3)
#     pyautogui.hotkey('alt', 'f4')