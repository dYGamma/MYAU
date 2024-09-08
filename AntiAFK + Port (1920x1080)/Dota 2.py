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

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

kb_controller = Controller()

hold_time = 5.0
pause_time = 2.5

is_moving = False

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

file_path = 'scr.ini'
config = configparser.ConfigParser()

if not config.read(file_path):
    config['scr'] = {'total_vb': '0'}
    with open(file_path, 'w') as configfile:
        config.write(configfile)

total_vb = int(config['scr'].get('total_vb', '0'))
session_vb = 0
keyboard = Controller()
search_area = (966, 487, 968, 489)
target_color = (126, 211, 33)
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
    

def update_video_frame():
    global cap, video_label, video_label_port, frame_interval
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
        
        video_label_port.config(image=photo)
        video_label_port.image = photo
        
        root.after(frame_interval, update_video_frame)
    else:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        root.after(frame_interval, update_video_frame)

def show_frame(frame):
    for widget in root.winfo_children():
        widget.grid_remove()
    frame.grid()

def on_enter(e):
    e.widget.config(bg="#555555")

def on_leave(e):
    e.widget.config(bg="#333333")

def create_button(frame, text, command, width, height):
    button = tk.Button(
        frame, text=text, command=command, width=width, height=height,
        bg="#333333", fg="#FFFFFF", font=("Helvetica", 12), relief="flat",
        activebackground="#555555", activeforeground="#FFFFFF",
        cursor="hand2"
    )
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    return button

root = tk.Tk()
root.title("")
root.configure(bg="#1E1E1E")
root.resizable(False, False)

root.geometry(f"304x550+{(root.winfo_screenwidth() - 304) // 2}+{(root.winfo_screenheight() - 550) // 2}")

frame1 = tk.Frame(root, bg="#1E1E1E")
frame2 = tk.Frame(root, bg="#1E1E1E")

frame1.grid(row=0, column=0, sticky="nsew")
frame2.grid(row=0, column=0, sticky="nsew")

start_button = create_button(frame1, "Старт", start_move, 10, 2)
start_button.pack(pady=10)

stop_button = create_button(frame1, "Стоп", stop_move, 10, 2)
stop_button.pack(pady=10)

port_button = create_button(frame1, "Порт | Схемы", lambda: show_frame(frame2), 15, 2)
port_button.pack(pady=10)

status_label = tk.Label(frame1, text="Статус: Остановлено", font=("Helvetica", 12), fg="lightcoral", bg="#1E1E1E")
status_label.pack(pady=10)

video_label = tk.Label(frame1, bg="#1E1E1E")
video_label.pack(pady=10)

back_button = create_button(frame2, "Назад", lambda: show_frame(frame1), 10, 2)
back_button.pack(pady=10)

start_button_port = create_button(frame2, "Запуск скрипта", start_script, 15, 2)
start_button_port.pack(pady=10)

stop_button_port = create_button(frame2, "Остановка скрипта", stop_script, 15, 2)
stop_button_port.pack(pady=10)

status_label_port = tk.Label(frame2, text="Статус скрипта: Остановлено", font=("Helvetica", 12), fg="lightcoral", bg="#1E1E1E")
status_label_port.pack(pady=10)

video_label_port = tk.Label(frame2, bg="#1E1E1E")
video_label_port.pack(pady=10)

show_frame(frame1)

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
