import os
import sys
import tkinter as tk
import cv2
from PIL import Image, ImageTk
from pynput.keyboard import Controller
import time
import threading

# Определение пути к встроенному файлу
def resource_path(relative_path):
    """ Получить путь к встроенному файлу. """
    try:
        # На первом этапе мы находимся в директории сборки
        base_path = sys._MEIPASS
    except AttributeError:
        # На этапе разработки
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

# Создаем контроллер для управления клавиатурой
kb_controller = Controller()

# Время между каждым шагом (в секундах)
hold_time = 5.0  # Время удержания клавиш
pause_time = 2.5  # Время между циклами

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
    status_label.config(text="Статус: Работает", fg="lightgreen")  # Обновляем статус на "Работает"
    print("Начинаю движение. Нажмите 'Стоп' для остановки.")
    
    while is_moving:
        for key_en, key_ru in directions:
            if not is_moving:
                break  # Прерываем цикл, если движение остановлено
            # Нажимаем обе клавиши, чтобы учесть обе раскладки
            kb_controller.press(key_en)
            kb_controller.press(key_ru)
            time_step = 0  # Временная переменная для таймера удержания
            while time_step < hold_time and is_moving:
                time.sleep(0.1)  # Пауза 0.1 сек для более частой проверки
                time_step += 0.1
            kb_controller.release(key_en)
            kb_controller.release(key_ru)
            time_step = 0
            while time_step < pause_time and is_moving:
                time.sleep(0.1)
                time_step += 0.1

    status_label.config(text="Статус: Остановлено", fg="lightcoral")  # Обновляем статус на "Остановлено"
    print("Движение остановлено.")

def start_move():
    global is_moving
    if not is_moving:
        threading.Thread(target=move_in_square).start()

def stop_move():
    global is_moving
    is_moving = False

def update_video_frame():
    global cap, video_label, frame_interval
    ret, frame = cap.read()
    if ret:
        # Уменьшаем размер видео в 2 раза
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
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Вернуться к началу видео
        root.after(frame_interval, update_video_frame)

# Создаем GUI
root = tk.Tk()
root.title("Управлялка ДуДимы")
root.configure(bg="#2E2E2E")  # Темный фон для окна

# Запрещаем изменение размера окна
root.resizable(False, False)

# Устанавливаем размеры окна
window_width = 304
window_height = 500
# Получаем размеры экрана
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Вычисляем позицию окна для центрирования
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Устанавливаем размер и позицию окна
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Создаем и размещаем кнопки на интерфейсе с темной темой
start_button = tk.Button(root, text="Старт", command=start_move, width=10, height=2, bg="#333333", fg="#00FF00", font=("Helvetica", 12))
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Стоп", command=stop_move, width=10, height=2, bg="#333333", fg="#FF0000", font=("Helvetica", 12))
stop_button.pack(pady=10)

# Создаем индикатор состояния
status_label = tk.Label(root, text="Статус: Остановлено", font=("Helvetica", 12), fg="lightcoral", bg="#2E2E2E")
status_label.pack(pady=10)

# Создаем метку для видео
video_label = tk.Label(root)
video_label.pack(pady=10)

# Открываем видео
video_path = resource_path('gul.mp4')
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Ошибка: Не удалось открыть видеофайл.")
    exit()

# Настройка параметров ускорения
fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0:
    print("Ошибка: FPS равен нулю. Проверьте видеофайл.")
    exit()

speed_up_factor = 5.0  # Ускорение в 5 раз (увеличьте значение для еще большего ускорения)
frame_interval = int(1000 / (fps * speed_up_factor))  # Интервал обновления кадров в миллисекундах

print(f"FPS: {fps}")
print(f"Frame interval: {frame_interval}")

# Запускаем обновление видео
update_video_frame()

# Запуск основного цикла Tkinter
root.mainloop()

# Освобождаем ресурсы после завершения
cap.release()

