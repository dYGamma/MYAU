import cv2
import numpy as np
import pyautogui
import time
import threading
import keyboard

# Настройки
screen_resolution = (1920, 1080)
toggle = False
step_check = 1
check = True
image_dir = 'img'  # Папка с изображениями
positions = [(0, 0)] * 20  # Позиции для 20 чисел

def image_search(image_path):
    screen = np.array(pyautogui.screenshot())
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    yloc, xloc = np.where(result >= 0.5)  # Пороговое значение для совпадения
    
    if len(xloc) > 0 and len(yloc) > 0:
        return xloc[0] + 20, yloc[0] + 20  # Возвращаем координаты
    return None

def bot_function():
    global toggle, step_check, check, positions
    
    while True:
        if not toggle:
            break
        time.sleep(0.1)
        
        if check:
            # Поиск изображений
            for i in range(20):
                img_path = f"{image_dir}/number_{i}.jpg"
                pos = image_search(img_path)
                if pos:
                    positions[i] = pos
                    step_check += 1
                    break
        else:
            # Клик по найденным позициям
            if step_check <= 20:
                pyautogui.click(positions[step_check - 1])
                time.sleep(1)
                step_check += 1
                if step_check > 20:
                    check = True
                    step_check = 1

def toggle_bot():
    global toggle, check, step_check
    toggle = not toggle
    check = True
    step_check = 1
    
    if toggle:
        threading.Thread(target=bot_function).start()

# Привязка клавиши F3 для активации/деактивации
keyboard.add_hotkey('F3', toggle_bot)

# Ожидание завершения программы
keyboard.wait('esc')  # Завершить программу при нажатии Esc
