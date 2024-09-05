import os
import sys
import tkinter as tk
import cv2
from PIL import Image, ImageTk
from pynput.keyboard import Controller
import time
import threading
import pyautogui
import configparser

# Определение пути к встроенному файлу
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

# Создаем контроллер для управления клавиатурой
kb_controller = Controller()

# Время между каждым шагом (в секундах)
hold_time = 5.0
pause_time = 2.5

# Флаг для остановки движения
is_moving = False

# Сопоставление клавиш для русской и английской раскладок
directions = [
    ('w', 'ц'),
    ('d', 'в'),
    ('s', 'ы'),
    ('a', 'ф')
]

def move_in_square():
    global is_moving
    is_moving = True
    status_label.config(text="Статус: Работает", fg="lightgreen")
    print("Начинаю движение. Нажмите 'Стоп' для остановки.")
    
    while is_moving:
        for key_en, key_ru in directions:
            if not is_moving:
                break
            kb_controller.press(key_en)
            kb_controller.press(key_ru)
            time_step = 0
            while time_step < hold_time and is_moving:
                time.sleep(0.1)
                time_step += 0.1
            kb_controller.release(key_en)
            kb_controller.release(key_ru)
            time_step = 0
            while time_step < pause_time and is_moving:
                time.sleep(0.1)
                time_step += 0.1

    status_label.config(text="Статус: Остановлено", fg="lightcoral")
    print("Движение остановлено.")

def start_move():
    global is_moving
    if not is_moving:
        threading.Thread(target=move_in_square, daemon=True).start()

def stop_move():
    global is_moving
    is_moving = False

# Конфигурация для второго скрипта
file_path = 'scr.ini'
config = configparser.ConfigParser()

if not config.read(file_path):
    config['scr'] = {'total_vb': '0'}
    with open(file_path, 'w') as configfile:
        config.write(configfile)

total_vb = int(config['scr'].get('total_vb', '0'))
session_vb = 0
keyboard = Controller()
search_area = (966, 487, 968, 489)  # x1, y1, x2, y2
target_color = (126, 211, 33)  # RGB-код цвета
running = False

def pixel_search_timer():
    global session_vb, total_vb
    while running:
        screenshot = pyautogui.screenshot(region=search_area)
        pixel = screenshot.getpixel((2, 2))

        if pixel == target_color:
            keyboard.press('e')
            keyboard.release('e')
            session_vb += 1
            total_vb += 1
            config['scr']['total_vb'] = str(total_vb)
            with open(file_path, 'w') as configfile:
                config.write(configfile)

        time.sleep(0.1)

def start_script():
    global running
    if not running:
        running = True
        threading.Thread(target=pixel_search_timer, daemon=True).start()
        status_label_port.config(text="Статус скрипта: Работает", fg="lightgreen")
        print('Скрипт запущен')

def stop_script():
    global running
    running = False
    status_label_port.config(text="Статус скрипта: Остановлено", fg="lightcoral")
    print(f'Скрипт выключен. Перенесено коробок - {session_vb}. Всего - {total_vb}')

def update_video_frame():
    global cap, video_label, frame_interval
    ret, frame = cap.read()
    if ret:
        height, width = frame.shape[:2]
        new_width = width // 2
        new_height = height // 2
        frame = cv2.resize(frame, (new_width, new_height))
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=image)
        video_label.config(image=photo)
        video_label.image = photo
        root.after(frame_interval, update_video_frame)
    else:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        root.after(frame_interval, update_video_frame)

def open_port_window():
    global port_window, status_label_port  # Объявляем глобальную переменную
    port_window = tk.Toplevel(root)
    port_window.title("Окно Порта")
    port_window.geometry("300x300")
    port_window.configure(bg="#2E2E2E")

    back_button = tk.Button(port_window, text="Назад", command=close_port_window, width=10, height=2, bg="#333333", fg="#00FF00", font=("Helvetica", 12))
    back_button.pack(pady=10)

    start_button_port = tk.Button(port_window, text="Запуск скрипта", command=start_script, width=15, height=2, bg="#333333", fg="#00FF00", font=("Helvetica", 12))
    start_button_port.pack(pady=10)

    stop_button_port = tk.Button(port_window, text="Остановка скрипта", command=stop_script, width=15, height=2, bg="#333333", fg="#FF0000", font=("Helvetica", 12))
    stop_button_port.pack(pady=10)

    status_label_port = tk.Label(port_window, text="Статус скрипта: Остановлено", font=("Helvetica", 12), fg="lightcoral", bg="#2E2E2E")
    status_label_port.pack(pady=10)

def close_port_window():
    global port_window
    port_window.destroy()

# Создаем GUI
root = tk.Tk()
root.title("Управлялка ДуДимы")
root.configure(bg="#2E2E2E")
root.resizable(False, False)

window_width = 304
window_height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x}+{y}")

start_button = tk.Button(root, text="Старт", command=start_move, width=10, height=2, bg="#333333", fg="#00FF00", font=("Helvetica", 12))
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Стоп", command=stop_move, width=10, height=2, bg="#333333", fg="#FF0000", font=("Helvetica", 12))
stop_button.pack(pady=10)

port_button = tk.Button(root, text="Порт", command=open_port_window, width=10, height=2, bg="#333333", fg="#00FFFF", font=("Helvetica", 12))
port_button.pack(pady=10)

status_label = tk.Label(root, text="Статус: Остановлено", font=("Helvetica", 12), fg="lightcoral", bg="#2E2E2E")
status_label.pack(pady=10)

video_label = tk.Label(root)
video_label.pack(pady=10)

video_path = resource_path('gul.mp4')
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Ошибка: Не удалось открыть видеофайл.")
    sys.exit()

fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0:
    print("Ошибка: FPS равен нулю. Проверьте видеофайл.")
    exit()

speed_up_factor = 5.0
frame_interval = int(1000 / (fps * speed_up_factor))

print(f"FPS: {fps}")
print(f"Frame interval: {frame_interval}")

update_video_frame()

root.mainloop()

cap.release()
