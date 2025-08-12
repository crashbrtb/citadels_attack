import pyautogui
import configparser
from pynput import mouse
import tkinter as tk
from screeninfo import get_monitors
file = 'positioncript.cfg'
scroll_count = 0
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
    config.read(file)
    config.set('COORDINATES', 'screen_area', str(res))

    # 7. Salvar as alterações no arquivo 'position.cfg'
    with open(file, 'w') as f:
        config.write(f)

def calibration(opt, msg, title, type_cap):
    # type_cap: 0 for area, 1 for clicks, 2 for scrolls and 3 for prompt
    cord_click = []
    howmany = int
    if type_cap == 3:
        howmany = int(pyautogui.prompt(text=msg, title=title, default=''))
    else:
        # 2. Abrir janela para gravar posição da torre de vigia
        pyautogui.alert(title=title, text=msg,
                        button="OK")
    if type_cap == 2:#how many scroll clicks capture
        scroll_capture()
    if type_cap == 1: #position Capture
        cord_click = get_click_postition()
        pyautogui.click(cord_click[0], cord_click[1])
        #print(cord_click)
    if type_cap == 0: #area capture
        cord_click = capture_area()
        pyautogui.click(cord_click[0] + 50, cord_click[1] + 20)

    config = configparser.ConfigParser()
    config.read(file)

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
    with open(file, 'w') as f:
        config.write(f)

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
    window_start = pyautogui.alert(title="Calibration", text="Follow the instructions in the next windows.",
                                   button="Start")
    get_monitor_resolution()
    #calibration("how_many_cripts", "Write down how many cripts you want to explorer:", "How Many Cripts", 3)
    #calibration("cord_click_watchtower","Let's capture the location of the Watch tower icon", "Watchtower", 1)
    #calibration("cord_click_cripts","Let's capture the location of the Cript menu", "Cript Menu",1)
    calibration("area_menu_button_go_cript", "Let's capture the go button inside cript area", "Cript go button", 0)
    calibration("center_of_screen","Let's capture the location of cript in center of map", "Cript in map",1)
    # comente cripta rara calibration("open_button","Let's capture the location of open button of cript", "Open Button",0)
    calibration("verify_if_open_explorer_button", "Let's capture the Explore icon area", "Explorer button icon", 0)
    calibration("cord_speedup_march", "Let's capture the location of speedup march button", "Speedup march",1)
    calibration("cord_click_use_speedups_screen", "Let's capture the speedups icon area", "Speedup icon", 0)
    calibration("cord_click_use_speedups", "Let's capture the location of use button", "Use Speedup button",1)
