import time
import os
import timeit
import cv2
import numpy as np
import pyautogui
from python_imagesearch.imagesearch import imagesearch_region_numLoop
import configparser

def click(x, y):
    pyautogui.click(x, y)
    time.sleep(2.0)


def move(x, y):
    pyautogui.moveTo(x, y)
    time.sleep(1.0)

def find_image_on_screen(caminho_imagem, area):
    # area of the screen to be captured initial xy and final xy
    ratio = 0.8
    time_wait = 0.0
    max_att = 5  # maximum number of attempts
    count = 0
    while True:
        pos = imagesearch_region_numLoop(caminho_imagem, time_wait, max_att, area[0], area[1], area[2], area[3], ratio)
        # print('Searching for watchtower menu')
        if pos[0] != -1:
            return pos
        count = count + 1
        if count > max_att:
            return False

def verify_store_screen(): #verify if store screen was open
    result = find_image_on_screen("images\\bonussale.png", screen_area)
    if result is None or result is False or len(result) == 0:
        return False
    else:
        posx = find_image_on_screen("images\\x.png", screen_area)  # if store was open, close it
        if posx is None or len(posx) == 0:
            return False
        else:
            click(screen_area[0] + posx[0] + 15, screen_area[1] + posx[1] + 15)
            return True

def list_files(directorys):

    files = []
    for directory in directorys:
        for raiz, _, files_directory in os.walk(directory):
            for file in files_directory:
                full_path = os.path.join(raiz, file)

                files.append((file, full_path))
    return files
def sleep_with_countdown(s):
    s = int(s)
    for i in reversed(range(s + 1)):
        print(i,end = " ")
        time.sleep(1)
    print('Time is over!')

def encontrar_centro_imagem_na_tela(icon):
    """
    Lê a configuração da área de captura de tela, tira um print,
    encontra uma imagem específica dentro do print e retorna as coordenadas do centro da imagem.
    """

    # 1. Ler a configuração do arquivo positioncript.cfg
    config = configparser.ConfigParser()
    config.read('positioncript.cfg')
    area_cript_icons = eval(config['COORDINATES']['area_cript_icons'])

    # 2. Tirar um print da tela conforme as coordenadas
    screenshot = pyautogui.screenshot(region=area_cript_icons)
    screenshot = np.array(screenshot)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)

    # 3. Carregar a imagem a ser procurada
    selected_cript = cv2.imread(icon, cv2.IMREAD_GRAYSCALE)
    h, w = selected_cript.shape

    # 4. Verificar se a imagem está contida no print da tela
    result = cv2.matchTemplate(screenshot_gray, selected_cript, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 5. Se a imagem for encontrada, calcular as coordenadas do centro
    threshold = 0.8  # Ajuste conforme necessário
    if max_val >= threshold:
        top_left = max_loc
        center_x = top_left[0] + w // 2 + area_cript_icons[0]
        center_y = top_left[1] + h // 2 + area_cript_icons[1]
        return center_x, center_y
    else:
        return None


if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read('positioncript.cfg')
    how_many_cripts = eval(config['COORDINATES']['how_many_cripts'])
    cord_click_watchtower = eval(config['COORDINATES']['cord_click_watchtower'])
    cord_click_cripts = eval(config['COORDINATES']['cord_click_cripts'])
    area_menu_button_go_cript = eval(config['COORDINATES']['area_menu_button_go_cript'])
    verify_if_open_explorer_button = eval(config['COORDINATES']['verify_if_open_explorer_button'])
    cord_speedup_march = eval(config['COORDINATES']['cord_speedup_march'])
    center_of_screen = eval(config['COORDINATES']['center_of_screen'])
    close_incorrect_windows = eval(config['COORDINATES']['close_incorrect_windows'])
    cord_click_use_speedups_screen = eval(config['COORDINATES']['cord_click_use_speedups_screen'])
    cord_click_use_speedups = eval(config['COORDINATES']['cord_click_use_speedups'])
    how_many_speedups = eval(config['COORDINATES']['how_many_speedups'])
    screen_area = eval(config['COORDINATES']['screen_area'])
    open_button = eval(config['COORDINATES']['open_button'])
    test = eval(config['COORDINATES']['test'])
    icon = 'images/cript/common/1.png'
    counter = 0 #Counter for cript
    errors = 0

    for i in range(how_many_cripts):
        # Using specific coordinates as there are many failures when identifying image or text
        #if verify_store_screen():
        if verify_store_screen(): #verify if store screen is open before start
            print("Store screen was close")
        click(cord_click_watchtower[0], cord_click_watchtower[1])
        click(cord_click_cripts[0], cord_click_cripts[1])
        pos = find_image_on_screen("images\\go.png",
                                   area_menu_button_go_cript)  # Search for go button on citadels list
        if pos is None or pos is False or len(pos) == 0:
            if verify_store_screen():  # if store open, verify and return True if store is closed or false if was false positive
                print("Store Screen Close")
            else:
                print("Go button not found, try again in 1 minutes")
                counter = counter - 1
                errors = errors + 1
                time.sleep(60.0)
                #break
        else:

            click(area_menu_button_go_cript[0] + pos[0] + 80, area_menu_button_go_cript[1] + pos[1] + 20) #click in go button
            #click in center or in differents points searching cripts
            center_control = 0
            while center_control < 9:
                if center_control > 0:
                    click(close_incorrect_windows[0],close_incorrect_windows[1]);
                click(center_of_screen[center_control][0], center_of_screen[center_control][1])
                #linha para cripta rara
                click(open_button[0], open_button[1])
                result = find_image_on_screen("images\\explore.png.", verify_if_open_explorer_button)
                if result is None or result is False or len(result) == 0:
                    print("Explorer button after store screen not found, search next point of click")
                else:
                    click(verify_if_open_explorer_button[0] + result[0] + 15, verify_if_open_explorer_button[1] + result[1] + 15)
                    time.sleep(2.0)  # Wait before clicking speed up, as
                    break
                center_control = center_control + 1
            if center_control < 9:
                    # sometimes the game takes a while to create the button
                click(cord_speedup_march[0], cord_speedup_march[1])  # click speedup
                result = find_image_on_screen("images\\troopsonthemarch.png.",
                                              cord_click_use_speedups_screen)  # Check if the
                # acceleration screen is really for the march to citadel
                if result is None or result is False or len(result) == 0:
                    print("Generic Error. Try again after 0,5 minutes")
                    errors = errors + 1
                    counter = counter - 1
                    time.sleep(1.0)
                    # break
                else:
                    for i in range(how_many_speedups):
                        click(cord_click_use_speedups[0], cord_click_use_speedups[1])  # acelera
                    start = timeit.default_timer()  # time counter
                    # verify if acceleration screen is open
                    while True:
                        result = find_image_on_screen("images\\troopsonthemarch.png.", cord_click_use_speedups_screen)
                        if result is None or result is False or len(result) == 0:
                            print("Troops screen closed")
                            break
                        else:
                            print("Waiting for the acceleration screen to close.")
                            time.sleep(5.0)
                    end = timeit.default_timer()  #
                    print('Duration: %f' % (end - start))
            else:
                print("Generic Error. Try again after 0,5 minutes")
                errors = errors + 1
                counter = counter - 1
                time.sleep(1.0)
            #sleep_with_countdown(end - start)  # Wait the same period of time for the screen to close, as the game
        counter = counter + 1
        print(counter, "/", how_many_cripts, " Cripts were explored")
        print(errors, " Errors was detected")