import tkinter as tk
from tkinter import messagebox
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import StandardScaler
import pandas as pd
import os

# Define the sequence globally
sequence = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]

# Define the sectors
def get_sector(number):
    if number == 0:
        return '0'
    elif 1 <= number <= 12:
        return '1-12'
    elif 13 <= number <= 24:
        return '13-24'
    elif 25 <= number <= 36:
        return '25-36'

def save_data(user_data):
    df = pd.DataFrame(user_data['positions'], columns=['Position'])
    df.to_csv('roulette_data.csv', index=False)

def load_data():
    if os.path.exists('roulette_data.csv'):
        df = pd.read_csv('roulette_data.csv')
        return df['Position'].tolist()
    return []

def train_and_predict_with_custom_data(user_data):
    np.random.seed(42)
    tf.random.set_seed(42)

    positions = np.array(user_data['positions'])

    if len(positions) < 2:
        raise ValueError("Должно быть как минимум два числа для обучения")

    X = []
    y = []

    for i in range(len(positions) - 1):
        X.append(positions[i])
        y.append(positions[i + 1])

    X = np.array(X).reshape(-1, 1)
    y = np.array(y)

    # Normalize input features
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # Ensure y fits the number of classes
    num_classes = len(sequence)
    labels = to_categorical(y, num_classes=num_classes)

    model = tf.keras.Sequential([
        layers.Dense(128, activation='relu', input_shape=(X.shape[1],)),
        layers.Dropout(0.5),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax')
    ])

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    # Train the model
    try:
        model.fit(x=X, y=labels, epochs=200, batch_size=16, verbose=1)  # Increased epochs and smaller batch size
    except Exception as e:
        raise RuntimeError(f"Ошибка при обучении модели: {str(e)}")

    # Predict the next positions
    last_position = np.array([[positions[-1]]])
    last_position = scaler.transform(last_position)  # Normalize last position
    predictions = model.predict(last_position)
    top_indices = np.argsort(predictions[0])[-3:]  # Get indices of the top 3 predictions
    top_positions = [sequence[i] for i in reversed(top_indices)]  # Get the corresponding positions
    top_sectors = [get_sector(pos) for pos in top_positions]

    return top_positions, top_sectors

# Tkinter UI
root = tk.Tk()
root.title("Roulette Prediction")

user_data = {'positions': load_data()}

def add_data():
    try:
        position = int(position_entry.get())
        if position not in sequence:
            raise ValueError("Неверное значение. Пожалуйста, введите число из последовательности.")
        user_data['positions'].append(position)
        position_entry.delete(0, tk.END)
        save_data(user_data)
        messagebox.showinfo("Data Added", "Data has been added.")
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def predict():
    if len(user_data['positions']) < 2:
        messagebox.showerror("Error", "Пожалуйста, введите как минимум два числа.")
        return

    try:
        top_positions, top_sectors = train_and_predict_with_custom_data(user_data)
        predictions = "\n".join(f"{pos} (Сектор: {sector})" for pos, sector in zip(top_positions, top_sectors))
        messagebox.showinfo("Prediction", f"Предсказанные следующие позиции:\n{predictions}")
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except RuntimeError as e:
        messagebox.showerror("Error", str(e))

tk.Label(root, text="Final Position:").pack()
position_entry = tk.Entry(root)
position_entry.pack()

tk.Button(root, text="Add Data", command=add_data).pack()
tk.Button(root, text="Predict Next", command=predict).pack()

root.mainloop()
