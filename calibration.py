import pyautogui
import configparser
from pynput import mouse
import tkinter as tk
from screeninfo import get_monitors
import os
import sys

scroll_count = 0

def get_base_path():
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def set_window_icon(window):
    candidates = ["icone.png", "icon.png"]
    search_paths = []

    # Current folder
    search_paths.append(os.getcwd())
    # Script folder (or _MEIPASS when frozen)
    search_paths.append(get_base_path())
    # Folder where executable is located
    search_paths.append(os.path.dirname(sys.executable))

    for base in search_paths:
        for icon_name in candidates:
            icon_path = os.path.join(base, icon_name)
            try:
                if os.path.exists(icon_path):
                    icon_image = tk.PhotoImage(file=icon_path)
                    window.iconphoto(True, icon_image)
                    # Keep reference to avoid garbage collection.
                    window._icon_image = icon_image
                    return
            except tk.TclError:
                pass


def center_window(window, width, height):
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


def show_info_dialog(title, message):
    result = {"ok": False}

    dialog = tk.Tk()
    dialog.title(title)
    dialog.resizable(False, False)
    set_window_icon(dialog)
    center_window(dialog, 460, 180)
    dialog.attributes("-topmost", True)

    tk.Label(dialog, text=message, wraplength=420, justify="center").pack(padx=20, pady=(24, 14))

    def on_ok():
        result["ok"] = True
        dialog.destroy()

    tk.Button(dialog, text="OK", command=on_ok, width=12).pack(pady=(0, 20))
    dialog.protocol("WM_DELETE_WINDOW", dialog.destroy)
    dialog.mainloop()
    return result["ok"]


def show_confirm_dialog(title, message, ok_text="OK", cancel_text="Cancel"):
    result = {"ok": False}

    dialog = tk.Tk()
    dialog.title(title)
    dialog.resizable(False, False)
    set_window_icon(dialog)
    center_window(dialog, 500, 200)
    dialog.attributes("-topmost", True)

    tk.Label(dialog, text=message, wraplength=460, justify="center").pack(padx=20, pady=(24, 14))

    buttons = tk.Frame(dialog)
    buttons.pack(pady=(0, 20))

    def on_ok():
        result["ok"] = True
        dialog.destroy()

    def on_cancel():
        result["ok"] = False
        dialog.destroy()

    tk.Button(buttons, text=ok_text, command=on_ok, width=12).pack(side="left", padx=8)
    tk.Button(buttons, text=cancel_text, command=on_cancel, width=12).pack(side="left", padx=8)

    dialog.protocol("WM_DELETE_WINDOW", on_cancel)
    dialog.mainloop()
    return result["ok"]


def show_prompt_dialog(title, message, default_value=""):
    result = {"value": None}

    dialog = tk.Tk()
    dialog.title(title)
    dialog.resizable(False, False)
    set_window_icon(dialog)
    center_window(dialog, 520, 220)
    dialog.attributes("-topmost", True)

    tk.Label(dialog, text=message, wraplength=480, justify="center").pack(padx=20, pady=(24, 10))

    entry = tk.Entry(dialog, width=32)
    entry.insert(0, default_value)
    entry.pack(pady=(0, 16))
    entry.focus_set()

    buttons = tk.Frame(dialog)
    buttons.pack(pady=(0, 20))

    def on_ok():
        value = entry.get().strip()
        result["value"] = value if value else None
        dialog.destroy()

    def on_cancel():
        result["value"] = None
        dialog.destroy()

    tk.Button(buttons, text="OK", command=on_ok, width=12).pack(side="left", padx=8)
    tk.Button(buttons, text="Cancel", command=on_cancel, width=12).pack(side="left", padx=8)

    dialog.bind("<Return>", lambda _event: on_ok())
    dialog.protocol("WM_DELETE_WINDOW", on_cancel)
    dialog.mainloop()
    return result["value"]


def choose_mode_dialog():
    result = {"mode": None}

    dialog = tk.Tk()
    dialog.title("Calibration")
    dialog.resizable(False, False)
    set_window_icon(dialog)
    center_window(dialog, 320, 190)
    dialog.attributes("-topmost", True)

    tk.Label(dialog, text="Select calibration mode:").pack(padx=20, pady=(20, 10))

    def choose(mode):
        result["mode"] = mode
        dialog.destroy()

    tk.Button(dialog, text="Full Calibration", width=20, command=lambda: choose("full")).pack(pady=5)
    tk.Button(dialog, text="Only Troops", width=20, command=lambda: choose("soldiers")).pack(pady=(5, 16))

    dialog.protocol("WM_DELETE_WINDOW", dialog.destroy)
    dialog.mainloop()
    return result["mode"]

def capture_area():
    def start_selection(event):
        nonlocal start_x, start_y
        start_x, start_y = event.x, event.y
        canvas.create_rectangle(start_x, start_y, start_x, start_y, outline='red', tag='selection')

    # Função para atualizar a seleção
    def update_selection(event):
        canvas.coords('selection', start_x, start_y, event.x, event.y)

    # Função para finalizar a seleção
    def end_selection(event):
        nonlocal area
        area = (start_x, start_y, event.x, event.y)
        window.destroy()  # Fecha a window

    # Criando a window
    area = None
    start_x = 0
    start_y = 0
    window = tk.Tk()
    window.title("Mouse Selection")
    set_window_icon(window)

    # Fazendo a window ocupar a tela inteira
    window.attributes('-fullscreen', True)
    # Tornando a window transparente
    window.attributes('-alpha', 0.3)

    # Criando o canvas
    canvas = tk.Canvas(window, width=window.winfo_screenwidth(), height=window.winfo_screenheight(), bg='white')
    canvas.pack()

    # Vinculando os eventos do mouse
    canvas.bind("<Button-1>", start_selection)
    canvas.bind("<B1-Motion>", update_selection)
    canvas.bind("<ButtonRelease-1>", end_selection)
    window.protocol("WM_DELETE_WINDOW", window.destroy)
    
    # Executando a window
    window.mainloop()
    return area

def get_click_postition():
    with mouse.Events() as events:
        for event in events:
            try:
                if event.button == mouse.Button.left:
                    return (event.x, event.y)
            except:
                pass

def scroll_capture():
        global scroll_count
        scroll_count = 0
        def on_scroll(x, y, dx, dy):
            global scroll_count
            scroll_count += dy

        def on_click(x, y, button, pressed):
            # Se o botão esquerdo do mouse for clicado, interrompe o listener
            if button == mouse.Button.left:
                return False

        # Inicia o listener do mouse
        with mouse.Listener(on_scroll=on_scroll, on_click=on_click) as listener:
            listener.join()
        return scroll_count
def get_monitor_resolution():
    monitors = get_monitors()
    resolutions = [(m.width, m.height) for m in monitors]
    res = (0,0,resolutions[0][0],resolutions[0][1])
    config = configparser.ConfigParser()
    config.read('position.cfg')
    config.set('COORDINATES', 'screen_area', str(res))

    # 7. Salvar as alterações no arquivo 'position.cfg'
    with open('position.cfg', 'w') as f:
        config.write(f)

def choose_calibration_mode():
    return choose_mode_dialog()

def calibration(opt, msg, title, type_cap):
    # type_cap: 0 for area, 1 for clicks, 2 for scrolls and 3 for prompt
    cord_click = []
    howmany = 0
    
    if type_cap == 3:
        val = show_prompt_dialog(title, msg, "")
        if val is None:
            raise SystemExit(0)
        try:
            howmany = int(val)
        except ValueError:
            show_info_dialog("Calibration", "Invalid number. Calibration canceled.")
            raise SystemExit(0)
            
    else:
        result = show_confirm_dialog(title, msg, "OK", "Cancel")
        if not result:
            raise SystemExit(0)
            
    if type_cap == 2:#how many scroll clicks capture
        scroll_capture()
    if type_cap == 1: #position Capture
        cord_click = get_click_postition()
        pyautogui.click(cord_click[0], cord_click[1])
        #print(cord_click)
    if type_cap == 0: #area capture
        cord_click = capture_area()
        if cord_click is None:
            raise SystemExit(0)
        #time.sleep(5)
        #print(cord_click[0],' ',cord_click[1],' ',cord_click[2],' ',cord_click[3])
        pyautogui.click(cord_click[0]+50, cord_click[1]+20)
        #print(cord_click[0]+50,' ',cord_click[1]+20)

    config = configparser.ConfigParser()
    config.read('position.cfg')

    # 6. Adicionar ou atualizar a coordenada no arquivo
    if not config.has_section('COORDINATES'):
        config.add_section('COORDINATES')
    if type_cap == 2:
        config.set('COORDINATES', opt, str(scroll_count*-1))#inverter sentido da rolagem, pois pynput captura a direção da rolagem diferente do piautogui
    elif type_cap == 3:
        config.set('COORDINATES', opt, str(howmany))
    else:
        config.set('COORDINATES', opt, str(cord_click))
        print(opt,"-",cord_click)

    # 7. Salvar as alterações no arquivo 'position.cfg'
    with open('position.cfg', 'w') as f:
        config.write(f)

    if opt == "cord_click_values_catapults":
        pyautogui.write(config.get("COORDINATES", "how_many_catapults"))
    if opt == "cord_click_values_troops":
        pyautogui.write(config.get("COORDINATES", "how_many_troops"))
    if opt == "cord_click_values_troops1":
        pyautogui.write(config.get("COORDINATES", "how_many_troops1"))
    if opt == "cord_click_values_troops2":
        pyautogui.write(config.get("COORDINATES", "how_many_troops2"))

    # Mensagem de sucesso
    if type_cap != 3:
        show_info_dialog("Calibration", "Position of the {} successfully captured!".format(title))
        
    if opt == "cord_click_use_speedups":
         show_info_dialog("Calibration", "Position of the {} successfully captured! Finished. All parameters were captured.".format(title))
def check_open_total_battle():
    """Checks if the Total Battle application is running."""

    # Find all windows with the given title
    window_title = "Total Battle"
    windows = pyautogui.getWindowsWithTitle(window_title)

    # If there's at least one window, activate it
    if windows:
        windows[0].restore()
        windows[0].maximize()
        windows[0].activate()
        print("Total Battle application is running!.")
        return True
    else:
        print("Total Battle application isn´t running.")
        return False


if __name__ == "__main__":
    try:
        if not check_open_total_battle():
            show_info_dialog(
                "Calibration",
                "Total Battle is not open. Please open the game and run calibration again."
            )
            raise SystemExit(0)

        mode = choose_calibration_mode()
        if mode is None:
            raise SystemExit(0)
    
        get_monitor_resolution()
    
        if mode == "full":
            calibration("how_many_citadels", "Write down how many citadels you want to attack:", "How Many Citadels", 3)
            calibration("cord_click_watchtower","Let's capture the location of the Watch tower icon", "Watchtower", 1)
            calibration("cord_click_monsters","Let's capture the location of the monsters menu", "Monsters Menu",1)
            calibration("cord_menu_button_go_citadels", "Let's capture the go button area", "Citatdel go button", 0)
            calibration("center_of_screen","Let's capture the location of citadel in center of map", "Citatel in map",1)
            calibration("verify_if_open_citadel", "Let's capture the citadel icon area", "Citatdel icon", 0)
            calibration("cord_attack_button","Let's capture the location of attack button", "Attack button", 1)
            calibration("scroll_to_soldiers", "Move the mouse to the list of troops and scroll until both catapults and other troops who you'll use are visible on the screen. Then click with the left mouse button", "Select Soldiers", 2)
            calibration("how_many_catapults", "Write down how many catapults you will use:", "Siege engine", 3)
            calibration("cord_click_values_catapults", "Let's capture the location of field to enter the number of catapults", "Siege engine", 1)
            calibration("how_many_troops", "Write down how many soldiers you will use:", "Troops Unit", 3)
            calibration("cord_click_values_troops", "Choose another troop type and click on the quantity field", "Troops Unit", 1)
            calibration("how_many_troops1", "Write down how many soldiers you will use:", "Troops1 Unit", 3)
            calibration("cord_click_values_troops1", "Choose another troop type and click on the quantity field", "Troops1 Unit", 1)
            calibration("how_many_troops2", "Write down how many soldiers you will use:", "Troops2 Unit", 3)
            calibration("cord_click_values_troops2", "Choose another troop type and click on the quantity field", "Troops3 Unit", 1)
            calibration("cord_startmarch_button", "Let's capture the location of start march button", "Start march",1)
            calibration("cord_speedup_march", "Let's capture the location of speedup march button", "Speedup march",1)
            calibration("cord_click_use_speedups_screen", "Let's capture the speedups icon area", "Speedup icon", 0)
            calibration("cord_click_use_speedups", "Let's capture the location of use button", "Use Speedup button",1)
        else:
            calibration("how_many_citadels", "Write down how many citadels you want to attack:", "How Many Citadels", 3)
            calibration("cord_attack_button","Let's capture the location of attack button", "Attack button", 1)
            calibration("scroll_to_soldiers", "Move the mouse to the list of troops and scroll until both catapults and other troops who you'll use are visible on the screen. Then click with the left mouse button", "Select Soldiers", 2)
            calibration("cord_click_values_catapults", "Let's capture the location of field to enter the number of catapults", "Siege engine", 1)
            calibration("cord_click_values_troops", "Choose another troop type and click on the quantity field", "Troops Unit", 1)
            calibration("cord_click_values_troops1", "Choose another troop type and click on the quantity field", "Troops1 Unit", 1)
            calibration("cord_click_values_troops2", "Choose another troop type and click on the quantity field", "Troops3 Unit", 1)

    except SystemExit:
        pass
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
