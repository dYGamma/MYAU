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
spin_interval = 4 * 60 * 60  # default 4 hours

directions = [
    ('w', 'ц'),
    ('d', 'в'),
    ('s', 'ы'),
    ('a', 'ф')
]

def spin_wheel():
    global spin_interval
    print("Скрипт начнет работу через 5 секунд...")
    time.sleep(5)
    
    while is_moving:
        pyautogui.press('up')
        time.sleep(1)
        
        pyautogui.moveTo(1832, 993, duration=1)
        pyautogui.click()
        time.sleep(1)

        pyautogui.moveTo(960, 450, duration=1)
        pyautogui.click()
        time.sleep(2)

        pyautogui.moveTo(645, 497, duration=1)
        pyautogui.click()
        time.sleep(2)

        pyautogui.moveTo(959, 901, duration=1)
        pyautogui.click()
        time.sleep(5)  

        pyautogui.press('esc')
        time.sleep(1)

        for _ in range(10):  
            pyautogui.press('w')
            time.sleep(1)
        
        print(f"Колесо прокручено, ожидание {spin_interval} секунд до следующего вращения.")
        time.sleep(spin_interval)

def move_in_square():
    global is_moving
    is_moving = True
    status_label.config(text="Статус: Работает", fg="lightgreen")
    print("Начинаю движение. Нажмите 'Стоп' для остановки.")

    threading.Thread(target=spin_wheel, daemon=True).start()
    
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
        
        root.after(10, update_video_frame)
    else:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        root.after(10, update_video_frame)

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

def apply_time_settings():
    global spin_interval
    try:
        hours = int(hours_entry.get())
        minutes = int(minutes_entry.get())
        seconds = int(seconds_entry.get())
        spin_interval = hours * 3600 + minutes * 60 + seconds
        print(f"Интервал прокрутки колеса установлен на {hours} часов {minutes} минут {seconds} секунд.")
        error_label.config(text=f"Время установлено на:\n{hours} ч. {minutes} мин. {seconds} сек.", fg="lightgreen")
        
    except ValueError:
        error_label.config(text="Ошибка:\nВремя некорректно", fg="lightcoral")
        print("Ошибка: время некорректно.")

def growing_circle(label):
    size = 1
    max_size = 10
    growing = True
    while True:
        if growing:
            size += 1
            if size >= max_size:
                growing = False
        else:
            size -= 1
            if size <= 1:
                growing = True
        
        circle = 'o' * size
        label.config(text=circle)
        root.update_idletasks()
        time.sleep(0.2)

root = tk.Tk()
root.title("")
root.configure(bg="#1E1E1E")
root.resizable(False, False)

root.geometry(f"304x795+{(root.winfo_screenwidth() - 304) // 2}+{(root.winfo_screenheight() - 795) // 2}")

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

settings_label = tk.Label(frame1, text="Настройки времени:", font=("Helvetica", 12), fg="lightgrey", bg="#1E1E1E")
settings_label.pack(pady=10)

time_frame = tk.Frame(frame1, bg="#1E1E1E")
time_frame.pack(pady=5)

hours_label = tk.Label(time_frame, text="Ч:", font=("Helvetica", 12), fg="lightgrey", bg="#1E1E1E")
hours_label.pack(side="left", padx=5)

hours_entry = tk.Entry(time_frame, width=5)
hours_entry.pack(side="left", padx=5)

minutes_label = tk.Label(time_frame, text="М:", font=("Helvetica", 12), fg="lightgrey", bg="#1E1E1E")
minutes_label.pack(side="left", padx=5)

minutes_entry = tk.Entry(time_frame, width=5)
minutes_entry.pack(side="left", padx=5)

seconds_label = tk.Label(time_frame, text="С:", font=("Helvetica", 12), fg="lightgrey", bg="#1E1E1E")
seconds_label.pack(side="left", padx=5)

seconds_entry = tk.Entry(time_frame, width=5)
seconds_entry.pack(side="left", padx=5)

apply_button = create_button(frame1, "Применить", apply_time_settings, 25, 2)
apply_button.pack(pady=10)

error_label = tk.Label(frame1, text="", font=("Helvetica", 12), fg="red", bg="#1E1E1E")
error_label.pack(pady=5)

video_label_port = tk.Label(frame2, bg="#1E1E1E")
video_label_port.pack(pady=10)

# Лейбл для анимации растущего круга (первая анимация)
circle_label1 = tk.Label(frame2, text="", font=("Helvetica", 14), fg="lightgrey", bg="#1E1E1E")
circle_label1.pack(pady=20)

# Лейбл для версии приложения
version_label = tk.Label(frame2, text="Версия: 1.1.0\nДата обновления: 15.09.2024", font=("Helvetica", 10), fg="lightgrey", bg="#1E1E1E")
version_label.pack(pady=20)

# Лейбл для второй анимации растущего круга
circle_label2 = tk.Label(frame2, text="", font=("Helvetica", 14), fg="lightgrey", bg="#1E1E1E")
circle_label2.pack(side="bottom", pady=10)

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

# Запуск анимации в отдельных потоках
threading.Thread(target=growing_circle, args=(circle_label1,), daemon=True).start()
threading.Thread(target=growing_circle, args=(circle_label2,), daemon=True).start()

root.mainloop()

cap.release()
