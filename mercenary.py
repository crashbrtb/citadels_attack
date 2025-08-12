import pyautogui
import cv2
import numpy as np
import winsound

# frequency is set to 500Hz
freq = 500

# duration is set to 100 milliseconds
dur = 500
# Função para verificar se a cor está presente em uma imagem
def check_color(img, color):
    # Convertemos a imagem para o espaço de cores HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Definimos os valores mínimos e máximos para a cor lilá no espaço HSV
    # Esses valores podem variar dependendo da tonalidade de lilá que você deseja detectar
    lower_purple = np.array([295, 45, 65])
    upper_purple = np.array([313, 64, 42])

    # Criamos uma máscara para os pixels que estão dentro do intervalo de cores
    mask = cv2.inRange(hsv, lower_purple, upper_purple)

    # Verificamos se há algum pixel branco na máscara (indicando a presença da cor)
    if np.any(mask == 255):
        return True
    else:
        return False

# Função principal
def main():
    while True:
        # Captura a tela
        screenshot = pyautogui.screenshot()

        # Converte a imagem PIL para um formato que o OpenCV pode usar
        open_cv_image = np.array(screenshot)
        open_cv_image = open_cv_image[:, :, ::-1].copy()

        # Verifica se a cor lilá está presente
        if check_color(open_cv_image, "purple"):
            print("Cor lilá encontrada!")
            winsound.Beep(freq, dur)

        # Adicione um delay para evitar sobrecarregar o processador
        pyautogui.sleep(1)

if __name__ == "__main__":
    main()