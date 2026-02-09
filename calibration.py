import pyautogui
import configparser
from pynput import mouse
import tkinter as tk
from screeninfo import get_monitors

def capture_area():
    def start_selection(event):
        global start_x, start_y
        start_x, start_y = event.x, event.y
        canvas.create_rectangle(start_x, start_y, start_x, start_y, outline='red', tag='selection')

    # Função para atualizar a seleção
    def update_selection(event):
        canvas.coords('selection', start_x, start_y, event.x, event.y)

    # Função para finalizar a seleção
    def end_selection(event):
        global area
        area = (start_x, start_y, event.x, event.y)
        window.destroy()  # Fecha a window

    # Criando a window
    window = tk.Tk()
    window.title("Mouse Selection")

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
    result = pyautogui.confirm(
        text="Select calibration mode:",
        title="Calibration",
        buttons=["Full Calibration", "Only Troops"]
    )
    if result == "Full Calibration":
        return "full"
    if result == "Only Troops":
        return "soldiers"
    return None

def calibration(opt, msg, title, type_cap):
    # type_cap: 0 for area, 1 for clicks, 2 for scrolls and 3 for prompt
    cord_click = []
    howmany = 0
    
    if type_cap == 3:
        val = pyautogui.prompt(text=msg, title=title, default='')
        if val is None or val.strip() == "":
            raise SystemExit(0)
        howmany = int(val)
            
    else:
        result = pyautogui.confirm(text=msg, title=title, buttons=["OK", "Cancel"])
        if result != "OK":
            raise SystemExit(0)
            
    if type_cap == 2:#how many scroll clicks capture
        scroll_capture()
    if type_cap == 1: #position Capture
        cord_click = get_click_postition()
        pyautogui.click(cord_click[0], cord_click[1])
        #print(cord_click)
    if type_cap == 0: #area capture
        cord_click = capture_area()
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
        pyautogui.alert(title="Calibration",
                        text="Position of the {} successfully captured!".format(title),
                        button="OK")
        
    if opt == "cord_click_use_speedups":
         pyautogui.alert(title="Calibration",
                        text="Position of the {} successfully captured! Finished. All parameters were captured.".format(title),
                        button="OK")



if __name__ == "__main__":
    try:
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
