import tkinter as tk
from tkinter import messagebox, filedialog
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import StandardScaler
import pandas as pd
import os
import pickle
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Последовательность чисел рулетки
sequence = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 
            8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 
            7, 28, 12, 35, 3, 26]

# Определение секторов
def get_sector(number):
    if number == 0:
        return '0'
    elif 1 <= number <= 12:
        return '1-12'
    elif 13 <= number <= 24:
        return '13-24'
    elif 25 <= number <= 36:
        return '25-36'

# Сохранение данных в CSV
def save_data(user_data):
    df = pd.DataFrame(user_data['positions'], columns=['Position'])
    df.to_csv('roulette_data.csv', index=False)

# Загрузка данных из CSV
def load_data():
    if os.path.exists('roulette_data.csv'):
        df = pd.read_csv('roulette_data.csv')
        return df['Position'].tolist()
    return []

# Подготовка данных для обучения
def prepare_data(positions, sequence_length=5):
    X, y = [], []
    for i in range(len(positions) - sequence_length):
        seq = positions[i:i + sequence_length]
        label = positions[i + sequence_length]
        X.append(seq)
        y.append(label)
    return np.array(X), np.array(y)

# Класс модели для управления обучением и предсказаниями
class RouletteModel:
    def __init__(self, sequence_length=5, model_path='roulette_model.h5', scaler_path='scaler.pkl'):
        self.sequence_length = sequence_length
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.model = None
        self.scaler = None
        self.num_classes = len(sequence)
        self._load_model()

    def _build_model(self):
        model = models.Sequential([
            layers.LSTM(128, activation='tanh', input_shape=(self.sequence_length, 1), return_sequences=True),
            layers.Dropout(0.3),
            layers.LSTM(64, activation='tanh'),
            layers.Dropout(0.3),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(self.num_classes, activation='softmax')
        ])

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return model

    def _load_model(self):
        if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
            self.model = models.load_model(self.model_path)
            with open(self.scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
            print("Модель и скейлер загружены.")
        else:
            self.model = self._build_model()
            self.scaler = StandardScaler()
            print("Создана новая модель и скейлер.")

    def train(self, positions, epochs=200, batch_size=16, callback=None):
        X, y = prepare_data(positions, self.sequence_length)

        # Преобразование категориальных меток
        y_encoded = to_categorical([sequence.index(num) for num in y], num_classes=self.num_classes)

        # Нормализация входных данных
        X_scaled = self.scaler.fit_transform(X)

        # Изменение формы для LSTM
        X_scaled = X_scaled.reshape((X_scaled.shape[0], self.sequence_length, 1))

        # Обучение модели
        if callback:
            self.model.fit(X_scaled, y_encoded, epochs=epochs, batch_size=batch_size, verbose=0, callbacks=[callback])
        else:
            self.model.fit(X_scaled, y_encoded, epochs=epochs, batch_size=batch_size, verbose=0)

        # Сохранение модели и скейлера
        self.model.save(self.model_path)
        with open(self.scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        print("Модель обучена и сохранена.")

    def predict_next(self, last_sequence, top_n=3):
        if self.model is None or self.scaler is None:
            raise ValueError("Модель не загружена.")

        last_sequence = np.array(last_sequence).reshape(1, -1)
        last_sequence_scaled = self.scaler.transform(last_sequence)
        last_sequence_scaled = last_sequence_scaled.reshape((1, self.sequence_length, 1))

        predictions = self.model.predict(last_sequence_scaled)
        top_indices = predictions[0].argsort()[-top_n:][::-1]
        top_probabilities = predictions[0][top_indices]
        top_positions = [sequence[i] for i in top_indices]
        top_sectors = [get_sector(pos) for pos in top_positions]

        return list(zip(top_positions, top_sectors, top_probabilities))

    def evaluate_model(self, positions):
        X, y = prepare_data(positions, self.sequence_length)
        y_encoded = to_categorical([sequence.index(num) for num in y], num_classes=self.num_classes)
        X_scaled = self.scaler.transform(X)
        X_scaled = X_scaled.reshape((X_scaled.shape[0], self.sequence_length, 1))
        loss, accuracy = self.model.evaluate(X_scaled, y_encoded, verbose=0)
        return loss, accuracy

# Callback для отображения прогресса обучения
class TrainingCallback(tf.keras.callbacks.Callback):
    def __init__(self, update_progress):
        super().__init__()
        self.update_progress = update_progress

    def on_epoch_end(self, epoch, logs=None):
        if logs is not None:
            self.update_progress(epoch + 1, logs.get('loss'), logs.get('accuracy'))

# Интерфейс Tkinter
class RouletteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Roulette Prediction")
        self.root.geometry("800x800")
        self.root.resizable(False, False)

        self.user_data = {'positions': load_data()}
        self.model = RouletteModel()

        # Если данных достаточно, обучить модель
        if len(self.user_data['positions']) >= self.model.sequence_length + 1:
            self.model.train(self.user_data['positions'])

        self.create_widgets()

    def create_widgets(self):
        # Меню
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Очистить данные", command=self.clear_data)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)

        # Верхний фрейм для ввода данных
        input_frame = tk.LabelFrame(self.root, text="Добавить число", padx=10, pady=10)
        input_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(input_frame, text="Введите число:").grid(row=0, column=0, padx=5, pady=5)
        self.position_entry = tk.Entry(input_frame, width=10)
        self.position_entry.grid(row=0, column=1, padx=5, pady=5)

        add_button = tk.Button(input_frame, text="Добавить число", command=self.add_data, bg="#4CAF50", fg="white")
        add_button.grid(row=0, column=2, padx=5, pady=5)

        # Фрейм для предсказаний
        predict_frame = tk.LabelFrame(self.root, text="Предсказать следующее число", padx=10, pady=10)
        predict_frame.pack(padx=10, pady=10, fill="x")

        predict_button = tk.Button(predict_frame, text="Предсказать", command=self.predict, bg="#2196F3", fg="white")
        predict_button.pack(pady=5)

        self.predictions_text = tk.Text(predict_frame, height=5, state='disabled')
        self.predictions_text.pack(pady=5, fill="x")

        # Фрейм для отображения последних введённых чисел
        data_frame = tk.LabelFrame(self.root, text="Последние числа", padx=10, pady=10)
        data_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.data_label = tk.Label(data_frame, text=self.get_recent_data(), justify="left", anchor="w")
        self.data_label.pack(fill="both", expand=True)

        # Фрейм для отображения точности модели
        model_info_frame = tk.LabelFrame(self.root, text="Информация о модели", padx=10, pady=10)
        model_info_frame.pack(padx=10, pady=10, fill="x")

        self.accuracy_label = tk.Label(model_info_frame, text="Точность модели: ")
        self.accuracy_label.pack(anchor="w")

        # Индикатор прогресса обучения
        self.progress_var = tk.DoubleVar()
        self.progress_bar = tk.ttk.Progressbar(model_info_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill="x", pady=5)

        self.status_label = tk.Label(model_info_frame, text="Статус: Готово")
        self.status_label.pack(anchor="w")

        # Фрейм для визуализации данных
        viz_frame = tk.LabelFrame(self.root, text="Визуализация данных", padx=10, pady=10)
        viz_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=viz_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.update_plot()

    def get_recent_data(self):
        recent = self.user_data['positions'][-10:]
        return ', '.join(map(str, recent)) if recent else "Нет данных"

    def add_data(self):
        try:
            position = int(self.position_entry.get())
            if position not in sequence:
                raise ValueError("Неверное значение. Введите число из последовательности.")
            self.user_data['positions'].append(position)
            self.position_entry.delete(0, tk.END)
            save_data(self.user_data)
            self.update_data_label()
            self.update_plot()
            messagebox.showinfo("Успех", f"Число {position} добавлено.")

            # Обучение модели с новыми данными
            if len(self.user_data['positions']) >= self.model.sequence_length + 1:
                self.train_model()

        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

    def predict(self):
        if len(self.user_data['positions']) < self.model.sequence_length:
            messagebox.showerror("Ошибка", f"Введите как минимум {self.model.sequence_length} чисел.")
            return
        try:
            last_sequence = self.user_data['positions'][-self.model.sequence_length:]
            predictions = self.model.predict_next(last_sequence)
            self.predictions_text.config(state='normal')
            self.predictions_text.delete(1.0, tk.END)
            for pos, sector, prob in predictions:
                self.predictions_text.insert(tk.END, f"{pos} (Сектор: {sector}) - Вероятность: {prob*100:.2f}%\n")
            self.predictions_text.config(state='disabled')
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

    def update_data_label(self):
        self.data_label.config(text=self.get_recent_data())

    def clear_data(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить все данные?"):
            self.user_data['positions'].clear()
            save_data(self.user_data)
            self.update_data_label()
            self.update_plot()
            self.predictions_text.config(state='normal')
            self.predictions_text.delete(1.0, tk.END)
            self.predictions_text.config(state='disabled')
            self.accuracy_label.config(text="Точность модели: ")
            if os.path.exists(self.model.model_path):
                os.remove(self.model.model_path)
            if os.path.exists(self.model.scaler_path):
                os.remove(self.model.scaler_path)
            self.model = RouletteModel()
            messagebox.showinfo("Успех", "Все данные очищены.")

    def train_model(self):
        try:
            self.status_label.config(text="Статус: Обучение...")
            self.progress_var.set(0)
            self.root.update_idletasks()

            callback = TrainingCallback(self.update_progress)
            # self.model.train(self.user_data['positions'], callback=callback)
            self.model.train(self.user_data['positions'], epochs=100, callback=callback)
            loss, accuracy = self.model.evaluate_model(self.user_data['positions'])
            self.accuracy_label.config(text=f"Точность модели на тренировочных данных: {accuracy*100:.2f}%")
            self.status_label.config(text="Статус: Обучение завершено.")
            self.progress_var.set(100)
        except Exception as e:
            self.status_label.config(text="Статус: Ошибка при обучении.")
            messagebox.showerror("Ошибка", f"Произошла ошибка при обучении модели: {str(e)}")

    def update_progress(self, epoch, loss, accuracy):
        # progress = (epoch / 200) * 100  # Предполагаем 200 эпох
        progress = (epoch / 100) * 100  # Предполагаем 200 эпох
        self.progress_var.set(progress)
        self.status_label.config(text=f"Статус: Обучение... Эпоха {epoch}/200")
        self.root.update_idletasks()

    def update_accuracy_label(self):
        if len(self.user_data['positions']) >= self.model.sequence_length + 1:
            try:
                loss, accuracy = self.model.evaluate_model(self.user_data['positions'])
                self.accuracy_label.config(text=f"Точность модели на тренировочных данных: {accuracy*100:.2f}%")
            except Exception as e:
                self.accuracy_label.config(text=f"Точность модели: Ошибка при оценке.")
        else:
            self.accuracy_label.config(text="Точность модели: Недостаточно данных для оценки.")

    def update_plot(self):
        self.ax.clear()
        if self.user_data['positions']:
            counts = pd.Series(self.user_data['positions']).value_counts().sort_index()
            self.ax.bar(counts.index, counts.values, color='skyblue')
            self.ax.set_xlabel('Число')
            self.ax.set_ylabel('Количество')
            self.ax.set_title('Распределение введённых чисел')
            self.ax.set_xticks(sequence)
        else:
            self.ax.text(0.5, 0.5, 'Нет данных для отображения', horizontalalignment='center', verticalalignment='center')
        self.canvas.draw()

# Запуск приложения
if __name__ == "__main__":
    # Импортируем ttk после создания root, чтобы избежать ошибок при использовании тем
    import tkinter.ttk as ttk

    root = tk.Tk()
    app = RouletteApp(root)
    root.mainloop()
