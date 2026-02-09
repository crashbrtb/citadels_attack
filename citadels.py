import time
import timeit
import cv2
import numpy as np
import pyautogui
import pytesseract
import tkinter as tk
import sys
from pynput import keyboard
from python_imagesearch.imagesearch import imagesearch_region_numLoop


stop_requested = False
stop_window = None
key_listener = None
log_text = None

def request_stop():
    global stop_requested
    stop_requested = True
    try:
        if stop_window is not None:
            stop_window.destroy()
    except:
        pass

def create_stop_window():
    global stop_window, log_text
    stop_window = tk.Tk()
    stop_window.title("Citatdels")
    stop_window.resizable(False, False)
    stop_window.attributes("-topmost", True)

    # Position bottom-right
    stop_window.update_idletasks()
    width = 320
    height = 220
    x = 20
    y = stop_window.winfo_screenheight() - height - 120
    stop_window.geometry(f"{width}x{height}+{x}+{y}")

    label = tk.Label(stop_window, text="Citatdels")
    label.pack(pady=(10, 5))
    btn = tk.Button(stop_window, text="Stop or ESC", command=request_stop, width=12)
    btn.pack(pady=(0, 10))

    log_frame = tk.Frame(stop_window)
    log_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    scrollbar = tk.Scrollbar(log_frame)
    scrollbar.pack(side="right", fill="y")
    log_text = tk.Text(log_frame, height=6, wrap="word", yscrollcommand=scrollbar.set)
    log_text.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=log_text.yview)

    class TextWriter:
        def write(self, message):
            if log_text is None:
                return
            log_text.insert("end", message)
            log_text.see("end")
        def flush(self):
            pass

    sys.stdout = TextWriter()
    sys.stderr = TextWriter()

    stop_window.protocol("WM_DELETE_WINDOW", request_stop)
    return stop_window

def start_keyboard_listener():
    global key_listener
    def on_press(key):
        if key == keyboard.Key.esc:
            request_stop()
            return False
    key_listener = keyboard.Listener(on_press=on_press)
    key_listener.daemon = True
    key_listener.start()

def check_stop():
    if stop_window is None:
        return False
    try:
        stop_window.update()
    except tk.TclError:
        return True
    return stop_requested

def sleep_with_stop(seconds):
    steps = max(1, int(seconds * 10))
    for _ in range(steps):
        if check_stop():
            raise SystemExit(0)
        time.sleep(0.1)

def click(x, y):
    pyautogui.click(x, y)
    sleep_with_stop(2.0)


def move(x, y):
    pyautogui.moveTo(x, y)
    sleep_with_stop(1.0)


def find_text_on_screen(texto, area):  # retun many errors, not used
    # area of the screen to be captured initial xy and final xy
    screenshot = np.array(pyautogui.screenshot(region=area))
    imagem = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    dados = pytesseract.image_to_data(imagem, output_type=pytesseract.Output.DICT)

    coordenadas = []
    for i in range(len(dados['text'])):
        if dados['text'][i] == texto:
            coordenadas.append((dados['left'][i] + area[0] + dados['width'][i] // 2,
                                dados['top'][i] + + area[1] + dados['height'][i] // 2))
            print(dados[i])
    return coordenadas

def check_open_total_battle():
    """Checks if the Total Battle application is running."""

    # Find all windows with the given title
    window_title = "Total Battle"
    windows = pyautogui.getWindowsWithTitle(window_title)

    # If there's at least one window, activate it
    if windows:
        windows[0].restore()
        windows[0].maximize()
        print("Total Battle application is running!.")
        return True
    else:
        print("Total Battle application isn´t running.")
        return False

def find_image_on_screen(caminho_imagem, area):
    # area of the screen to be captured initial xy and final xy
    ratio = 0.6
    time_wait = 0.0
    max_att = 3  # maximum number of attempts
    count = 0
    while True:
        pos = imagesearch_region_numLoop(caminho_imagem, time_wait, max_att, area[0], area[1], area[2], area[3], ratio)
        # print('Searching for watchtower menu')
        if pos[0] != -1:
            return pos
        count = count + 1
        if count > max_att:
            break


def sleep_with_countdown(s):
    s = int(s)
    for i in reversed(range(s + 1)):
        print(i,end = " ")
        sleep_with_stop(1)
    print('Time is over!')

def verify_store_screen(): #verify if store screen was open
    result = find_image_on_screen("images\\bonussale.png", screen_area)
    if result is None or len(result) == 0:
        return False
    else:
        posx = find_image_on_screen("images\\x.png", screen_area)  # if store was open, close it
        if posx is None or len(posx) == 0:
            return False
        else:
            click(screen_area[0] + posx[0] + 15, screen_area[1] + posx[1] + 15)
            return True


if __name__ == "__main__":
    global_vars = {}
    with open('position.cfg', 'r') as f:
        for line in f:
            if line.strip():  # Ignora linhas vazias
                if line.startswith('['):
                    print("") #just to ignore name of section
                else:
                    var, value = line.split('=')
                    var = var.strip()  # Remove espaços em branco antes e depois do nome da variável
                    value = value.strip()  # Remove espaços em branco antes e depois do valor

                    # Convert value (int, tuple ou str)
                    if value.isdigit():
                        value = int(value)
                    elif value.startswith('(') and value.endswith(')'):
                        value = tuple(map(int, value[1:-1].split(',')))
                    elif value.startswith('str(') and value.endswith(')'):
                        value = str(value[4:-1])

                    # put value to global_vars
                    global_vars[var] = value

    how_many_citadels = global_vars['how_many_citadels']
    cord_click_watchtower = global_vars['cord_click_watchtower']
    cord_click_monsters = global_vars['cord_click_monsters']
    cord_menu_button_go_citadels = global_vars['cord_menu_button_go_citadels']
    verify_if_open_citadel = global_vars['verify_if_open_citadel']
    center_of_screen = global_vars['center_of_screen']
    cord_attack_button = global_vars['cord_attack_button']
    scroll_to_soldiers = global_vars['scroll_to_soldiers']
    cord_click_values_catapults = global_vars['cord_click_values_catapults']
    how_many_catapults = global_vars['how_many_catapults']  # To use them all, use a very large value
    cord_click_values_troops = global_vars['cord_click_values_troops']
    how_many_troops = global_vars['how_many_troops']  # To use them all, use a very large value
    cord_click_values_troops1 = global_vars['cord_click_values_troops1']
    how_many_troops1 = global_vars['how_many_troops1']  # To use them all, use a very large value
    cord_click_values_troops2 = global_vars['cord_click_values_troops2']
    how_many_troops2 = global_vars['how_many_troops2']  # To use them all, use a very large value
    cord_startmarch_button = global_vars['cord_startmarch_button'] # location of the attack button on the citadel screen
    cord_speedup_march = global_vars['cord_speedup_march']  # location of button speedup march
    how_many_speedups = global_vars['how_many_speedups']  # How many accelerators do you want to use?
    cord_click_use_speedups = global_vars['cord_click_use_speedups']
    cord_click_use_speedups_screen = global_vars['cord_click_use_speedups_screen']
    screen_area = global_vars['screen_area']
    test = bool(global_vars['test'])
    counter = 0 #Counter for citadels
    errors = 0

    create_stop_window()
    start_keyboard_listener()
    for i in range(how_many_citadels):
        if check_stop():
            break
        # Using specific coordinates as there are many failures when identifying image or text
        if verify_store_screen(): #verify if store screen is open before start
            click(center_of_screen[0], center_of_screen[1])
        else:
            click(center_of_screen[0], center_of_screen[1])
        click(cord_click_watchtower[0], cord_click_watchtower[1])
        click(cord_click_monsters[0], cord_click_monsters[1])
        check_open_total_battle(); #verify if total battle is open and/or maximized
        pos = find_image_on_screen("images\\go.png", cord_menu_button_go_citadels)#Search for go button on citadels list
        if pos is None or len(pos) == 0:
            if verify_store_screen(): #if store open, verify and return True if store is closed or false if was false positive
                posb = find_image_on_screen("images\\go.png",
                                               cord_menu_button_go_citadels)  # Search for go button on citadels list
                if posb is None or len(posb) == 0:
                    print("There arent more citadels")
                    errors = errors + 1
                    counter = counter - 1
                    #break
                else:
                    click(cord_menu_button_go_citadels[0] + pos[0] + 80, cord_menu_button_go_citadels[1] + pos[1] + 20)
                    print("clicando no botão go")
            else:
                print("Go button not found, try again in 5 minutes")
                counter = counter - 1
                errors = errors + 1
                sleep_with_stop(600.0)
                #break
        else:
            click(cord_menu_button_go_citadels[0] + pos[0] + 80, cord_menu_button_go_citadels[1] + pos[1] + 20) #click in go button
            if verify_store_screen():
                click(center_of_screen[0], center_of_screen[1])
            else:
                click(center_of_screen[0], center_of_screen[1])
            #result = find_image_on_screen("images\\watchtower\\cursedcitadel.png.", verify_if_open_citadel)
            result = find_image_on_screen("images\\watchtower\\elfcitadel.png.", verify_if_open_citadel)
            if result is None or len(result) == 0:
                if verify_store_screen():
                    click(cord_attack_button[0], cord_attack_button[1])
                else:
                    print("Citatel icon not found, try again")
                    errors = errors + 1
                    counter = counter - 1
            else:

                click(cord_attack_button[0], cord_attack_button[1])
                pyautogui.move(-120, 0) #position curson inside of troops selection
                for i in range(scroll_to_soldiers):
                    pyautogui.scroll(-100)
                click(cord_click_values_catapults[0], cord_click_values_catapults[1])  # click on the catapult troop quantity field
                pyautogui.write(str(how_many_catapults))
                click(cord_click_values_troops[0], cord_click_values_troops[1])  # click on the melee troop quantity field
                pyautogui.write(str(how_many_troops))
                click(cord_click_values_troops1[0], cord_click_values_troops1[1])  # click on the melee troop quantity field
                pyautogui.write(str(how_many_troops1))
                click(cord_click_values_troops2[0], cord_click_values_troops2[1])  # click on the melee troop quantity field
                pyautogui.write(str(how_many_troops2))
                if test:
                    print("Test finish")
                    break
                click(cord_startmarch_button[0], cord_startmarch_button[1])  # click start march button
                sleep_with_stop(2.0)  # Wait before clicking speed up, as sometimes the game takes a while to create the button
                click(cord_speedup_march[0], cord_speedup_march[1])  # click speedup
                result = find_image_on_screen("images\\troopsonthemarch.png.",cord_click_use_speedups_screen)  # Check if the
                # acceleration screen is really for the march to citadel
                if result is None or len(result) == 0:
                    print("Generic Error. Try again after 0,5 minutes")
                    errors = errors + 1
                    counter = counter - 1
                    sleep_with_stop(30.0)
                    #break
                else:
                    for i in range(how_many_speedups):
                        click(cord_click_use_speedups[0], cord_click_use_speedups[1])  # acelera
                    start = timeit.default_timer()  # time counter
                    # verify if acceleration screen is open
                    while True:
                        result = find_image_on_screen("images\\troopsonthemarch.png.",cord_click_use_speedups_screen)
                        if result is None or len(result) == 0:
                            print("Troops scree1200n closed")
                            break
                        else:
                            print("Waiting for the acceleration screen to close.")
                            sleep_with_stop(5.0)
                    end = timeit.default_timer()  #
                    print('Duration: %f' % (end - start))
                    sleep_with_countdown(end - start)  # Wait the same period of time for the screen to close, as the game

                    # eventually closes the screen when troops arrive at the citadel instead of closing
                    # it when they return to the city

        counter = counter + 1
        print(counter, "/", how_many_citadels, " citadels were destroyed")
        print(errors, " Errors was detected")