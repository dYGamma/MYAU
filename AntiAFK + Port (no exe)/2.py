import mss
import numpy as np
import cv2
from PIL import Image, ImageTk
import pytesseract
import time
import threading
import tkinter as tk
from pynput.keyboard import Controller

# Убедитесь, что pytesseract установлен
pytesseract.pytesseract.tesseract_cmd = r"E:\auto\tes\tesseract.exe"

# Создаем контроллер для управления клавиатурой
kb_controller = Controller()

# Время между каждым шагом (в секундах)
hold_time = 0.0  # Время удержания клавиши
pause_time = 1.5  # Пауза между циклами

# Флаг для остановки движения
is_moving = False

# Функция для распознавания букв
def detect_keys(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape

    # Захватываем центральную область экрана
    center_area = gray[h // 2 - 100:h // 2 + 100, w // 2 - 100:w // 2 + 100]

    # Используем pytesseract для распознавания текста
    detected_text = pytesseract.image_to_string(center_area, config='--psm 6')
    detected_text = detected_text.lower()  # Приводим текст к нижнему регистру

    
    return {
        'e': 'e' in detected_text or 'E' in detected_text,
        'y': 'y' in detected_text or 'Y' in detected_text,
        'f': 'f' in detected_text or 'F' in detected_text,
        'd': 'd' in detected_text or 'D' in detected_text,
    }

# Движение в зависимости от распознанных букв с учетом времени удержания
def move_based_on_detection(detected_keys):
    for key, pressed in detected_keys.items():
        if pressed:
            kb_controller.press(key)
            time.sleep(hold_time)  # Удержание клавиши
            kb_controller.release(key)
        time.sleep(pause_time)  # Пауза между нажатиями

# Запуск отслеживания
def start_detection():
    global is_moving
    is_moving = True
    status_label.config(text="Статус: Работает", fg="lightgreen")
    
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Выбираем первый монитор

        while is_moving:
            screenshot = sct.grab(monitor)
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            detected_keys = detect_keys(frame)
            move_based_on_detection(detected_keys)
            time.sleep(0.1)  # Небольшая задержка перед следующим циклом

    status_label.config(text="Статус: Остановлено", fg="lightcoral")

# Старт и стоп функций отслеживания
def start_move():
    global is_moving
    if not is_moving:
        threading.Thread(target=start_detection).start()

def stop_move():
    global is_moving
    is_moving = False

# Обновление GUI
def update_video_frame():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        image = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=image)
        video_label.config(image=photo)
        video_label.image = photo
        root.after(10, update_video_frame)

# Создаем GUI
root = tk.Tk()
root.title("Управлялка ДуДимы")
root.configure(bg="#2E2E2E")
root.resizable(False, False)

# Сделать окно поверх всех окон
# root.attributes("-topmost", True)

# Настройка размера окна
window_width = 304
window_height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Кнопки управления
start_button = tk.Button(root, text="Старт", command=start_move, width=10, height=2, bg="#333333", fg="#00FF00", font=("Helvetica", 12))
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Стоп", command=stop_move, width=10, height=2, bg="#333333", fg="#FF0000", font=("Helvetica", 12))
stop_button.pack(pady=10)

# Индикатор состояния
status_label = tk.Label(root, text="Статус: Остановлено", font=("Helvetica", 12), fg="lightcoral", bg="#2E2E2E")
status_label.pack(pady=10)

# Метка для отображения видео
video_label = tk.Label(root)
video_label.pack(pady=10)

# Запуск обновления видео
update_video_frame()

# Запуск основного цикла Tkinter
root.mainloop()





