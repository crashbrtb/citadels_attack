
import pyautogui
import time
from screeninfo import get_monitors
from python_imagesearch.imagesearch import imagesearch_region_numLoop


window_title = "Total Battle"
path_total_battle = "C:\\Users\\clesi\\AppData\\Roaming\\Scorewarrior\\TotalBattle\\Launcher.exe"
coords_play_button = (934,789)

def open_laucher_total_battle():
        print("Total Battle Starting...")
        # Command to start the application
        pyautogui.hotkey('win', 'r')  # Opens the Run dialog
        pyautogui.write(path_total_battle)
        pyautogui.press('enter')
        # Wait a few seconds for the application to load
        time.sleep(10)
        print("Laucher Total Battle is running!")
        return True
def check_open_total_battle():
    """Checks if the Total Battle application is running."""

    # Find all windows with the given title
    windows = pyautogui.getWindowsWithTitle(window_title)

    # If there's at least one window, activate it
    if windows:
        windows[0].restore()
        windows[0].activate()
        print("Total Battle application is running!.")
        return True
    else:
        print("Total Battle application isn´t running.")
        return False

def get_monitor_resolution():
    monitors = get_monitors()
    resolutions = [(m.width, m.height) for m in monitors]
    res = (0,0,resolutions[0][0],resolutions[0][1])
    return res
def close_store(screen_area): #verify if store screen was open
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
def find_image_on_screen(path_image, area):
    # area of the screen to be captured initial xy and final xy
    ratio = 0.6
    time_wait = 0.0
    max_att = 5  # maximum number of attempts
    count = 0
    while True:
        pos = imagesearch_region_numLoop(path_image, time_wait, max_att, area[0], area[1], area[2], area[3], ratio)
        # print('Searching for watchtower menu')
        if pos[0] != -1:
            return pos
        count = count + 1
        if count > max_att:
            break
def click(x, y):
    pyautogui.click(x, y)
    time.sleep(2.0)
def start_counter():
    print("put here code for starting counter")

if __name__ == "__main__":
    if check_open_total_battle():
        if close_store(get_monitor_resolution()):
            start_counter() #Execute counter
        else:
            print("Store wasn´t open ")
            start_counter()  # Execute counter
    elif open_laucher_total_battle():
        click(coords_play_button[0],coords_play_button[1])
        print("Click play button")
        time.sleep(10.0)
        close_store(get_monitor_resolution())
        if check_open_total_battle():
            start_counter()  # Execute counter
        else:
            print("Error01! Cannot open Total Battle")
    else:
        print("Error02! Cannot open Total Battle")

