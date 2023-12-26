import pyautogui
import pytesseract
import keyboard
import time
import configparser
import os
import sys
import concurrent.futures

CONFIG_FILE_PATH = 'config.ini'

def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

def show_main_menu():
    print("\nDota 2 AutoArmlet by DeadRound\n")
    print("1 - Start")
    print("2 - Settings")
    print("3 - Exit")


def show_settings_menu():
    print("\nSettings Menu:\n")
    print("1 - Armlet Key")
    print("2 - Processor Threads")
    print("3 - Exit Key")
    print("4 - Min Percent Of HP")
    print("5 - PyTesseract Folder")
    print("6 - Coords Changer")
    print("7 - Back")


def get_user_input(prompt):
    return input(prompt)


def get_config_path():
    return CONFIG_FILE_PATH


def load_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config


def save_setting(setting_name, value):
    config = load_config(get_config_path())
    if 'Settings' not in config:
        config['Settings'] = {}
    config['Settings'][setting_name] = str(value)
    with open(get_config_path(), 'w') as config_file:
        config.write(config_file)

last_press_time = time.time()

def start_auto_armlet():
    global last_press_time

    with concurrent.futures.ThreadPoolExecutor(max_workers=processor_threads) as executor:
        while True:
            screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
            raw_text = pytesseract.image_to_string(screenshot, lang='eng')
            print(raw_text)

            split_text = raw_text.split("/")
            if len(split_text) == 2:
                text1, text2 = map(str.strip, split_text)
                try:
                    num1, num2 = map(int, (text1, text2))
                    difference = num2 - num1

                    if num1 <= min_percent_of_hp * num2:
                        current_time = time.time()
                        if current_time - last_press_time > 0.5:
                            keyboard.press_and_release(armlet_key)
                            keyboard.press_and_release(armlet_key)
                            print(f"Pressed '{armlet_key}' twice.")
                            last_press_time = current_time


                    print("Number 1:", num1)
                    print("Number 2:", num2)
                    print("Difference:", difference)

                except ValueError:
                    print("Error: Could not convert text to numbers.")

            if keyboard.is_pressed(exit_key):
                break

def get_min_percent_of_hp():
    config = load_config(get_config_path())
    return float(config.get('Settings', 'MinPercentOfHP', fallback=0.2))


def get_pytesseract_folder():
    config = load_config(get_config_path())
    return str(config.get('Settings', 'PyTesseractFolder', fallback=''))


def get_armlet_key():
    config = load_config(get_config_path())
    return config.get('Settings', 'ArmletKey', fallback='x')


def get_processor_threads():
    config = load_config(get_config_path())
    return int(config.get('Settings', 'ProcessorThreads', fallback='2'))


def get_exit_key():
    config = load_config(get_config_path())
    return str(config.get('Settings', 'ExitKey', fallback='u'))


def get_new_setting():
    config = load_config(get_config_path())
    return config.get('Settings', 'NewSetting', fallback='default_value_for_new_setting')


def get_coords():
    config = load_config(get_config_path())
    x1 = int(config.get('Settings', 'X1', fallback='767'))
    y1 = int(config.get('Settings', 'Y1', fallback='1013'))
    x2 = int(config.get('Settings', 'X2', fallback='1047'))
    y2 = int(config.get('Settings', 'Y2', fallback='1046'))
    return x1, y1, x2, y2


def save_coords(x1, y1, x2, y2):
    config = load_config(get_config_path())
    config['Settings']['X1'] = str(x1)
    config['Settings']['Y1'] = str(y1)
    config['Settings']['X2'] = str(x2)
    config['Settings']['Y2'] = str(y2)
    with open(get_config_path(), 'w') as config_file:
        config.write(config_file)


min_percent_of_hp = get_min_percent_of_hp()
armlet_key = get_armlet_key()
pytesseract_folder = get_pytesseract_folder()
pytesseract.pytesseract.tesseract_cmd = pytesseract_folder
processor_threads = get_processor_threads()
exit_key = get_exit_key()
new_setting = get_new_setting()
x1, y1, x2, y2 = get_coords()

def main():
    while True:
        show_main_menu()
        choice_main = get_user_input("Select an option: ")

        if choice_main == '1':
            start_auto_armlet()

        elif choice_main == '2':
            while True:
                show_settings_menu()
                choice_settings = get_user_input("Select a setting: ")

                if choice_settings == '1':
                    armlet_key = get_user_input("Armlet Key: ")
                    save_setting('ArmletKey', armlet_key)

                elif choice_settings == '2':
                    processor_threads = get_user_input("Number of Processor Threads: ")
                    save_setting('ProcessorThreads', processor_threads)

                elif choice_settings == '3':
                    exit_key = get_user_input("Exit Key: ")
                    save_setting('ExitKey', exit_key)

                elif choice_settings == '4':
                    min_percent_of_hp = get_user_input("Minimum Hero's HP Percentage: ")
                    save_setting('MinPercentOfHP', int(min_percent_of_hp) / 100)

                elif choice_settings == '5':
                    pytesseract_folder = get_user_input("PyTesseract Folder Without \"\": ")
                    save_setting('PyTesseractFolder', pytesseract_folder)
                    pytesseract.pytesseract.tesseract_cmd = pytesseract_folder

                elif choice_settings == '6':
                    print("Press F8 Twice To Choose HP Coordinates.")
                    keyboard.wait('F8', suppress=True)
                    x1, y1 = pyautogui.position()
                    print(f"Saved Coordinates: X1={x1}, Y1={y1}")
                    keyboard.wait('F8', suppress=True)
                    x2, y2 = pyautogui.position()
                    print(f"Saved Coordinates: X2={x2}, Y2={y2}")
                    save_coords(x1, y1, x2, y2)

                elif choice_settings == '7':
                    restart_program()
                    break

                else:
                    print("Invalid choice. Please try again.")

        elif choice_main == '3':
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()