import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os

# Константы
JSON_FILE = "password_history.json"
MIN_LENGTH = 4
MAX_LENGTH = 32

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных паролей")
        self.root.geometry("600x450")

        # Переменные
        self.length_var = tk.IntVar(value=12)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_letters = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=True)

        self.create_widgets()
        self.load_history()

    def create_widgets(self):
        # --- Верхняя панель (Настройки) ---
        frame_settings = ttk.LabelFrame(self.root, text="Настройки пароля", padding="10")
        frame_settings.pack(fill="x", padx=10, pady=5)

        # Длина пароля
        ttk.Label(frame_settings, text="Длина:").grid(row=0, column=0, sticky="w")
        self.slider_length = ttk.Scale(
            frame_settings,
            from_=MIN_LENGTH,
            to=MAX_LENGTH,
            orient="horizontal",
            variable=self.length_var,
            command=self.update_length_label
        )
        self.slider_length.grid(row=0, column=1, sticky="ew")

        self.label_length = ttk.Label(frame_settings, text=f"Текущая длина: {self.length_var.get()}")
        self.label_length.grid(row=0, column=2, padx=10)

        # Чекбоксы символов
        ttk.Checkbutton(frame_settings, text="Цифры", variable=self.use_digits).grid(row=1, column=0, sticky="w")
        ttk.Checkbutton(frame_settings, text="Буквы", variable=self.use_letters).grid(row=1, column=1, sticky="w")
        ttk.Checkbutton(frame_settings, text="Спецсимволы", variable=self.use_special).grid(row=1, column=2, sticky="w")

        # Кнопка генерации
        ttk.Button(self.root, text="Сгенерировать пароль", command=self.generate_password).pack(pady=15)

        # --- Поле вывода пароля ---
        self.password_entry = ttk.Entry(self.root, width=50, font=("Arial", 12))
        self.password_entry.pack(pady=5)

        # --- История ---
        frame_history = ttk.LabelFrame(self.root, text="История", padding="5")
        frame_history.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(frame_history, columns=("password", "length"), show="headings")
        self.tree.heading("password", text="Пароль")
        self.tree.heading("length", text="Длина")
        self.tree.column("password", width=300)
        self.tree.column("length", width=80)
        
        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(frame_history, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def update_length_label(self, val):
        self.label_length.config(text=f"Текущая длина: {int(float(val))}")

    def generate_password(self):
        length = self.length_var.get()
        
        # Валидация: хотя бы один тип символов выбран
        if not (self.use_digits.get() or self.use_letters.get() or self.use_special.get()):
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов (цифры, буквы или спецсимволы)")
            return

        chars = ""
        if self.use_digits.get():
            chars += string.digits
        if self.use_letters.get():
            chars += string.ascii_letters
        if self.use_special.get():
            chars += string.punctuation

        password = ''.join(random.choices(chars, k=length))
        
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        
        # Добавление в историю (в начало списка)
        self.history.insert(0, {"password": password, "length": length})
        
        # Обновление таблицы (показываем только последние 10 записей для удобства)
        self.update_treeview()
        
    def update_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        for item in self.history[:10]:  # Показываем максимум 10 последних
            self.tree.insert("", "end", values=(item["password"], item["length"]))
            
    def load_history(self):
         # Загрузка истории из JSON при запуске
         if os.path.exists(JSON_FILE):
             try:
                 with open(JSON_FILE, "r", encoding="utf-8") as f:
                     data = json.load(f)
                     if isinstance(data, list):
                         self.history = data
                     else:
                         self.history = []
             except Exception as e:
                 messagebox.showerror("Ошибка чтения файла", f"Не удалось загрузить историю: {e}")
                 self.history = []
         else:
             self.history = []
             
    def save_history(self):
         try:
             with open(JSON_FILE, "w", encoding="utf-8") as f:
                 json.dump(self.history, f, ensure_ascii=False, indent=2)
         except Exception as e:
             messagebox.showerror("Ошибка записи файла", f"Не удалось сохранить историю: {e}")

    def on_closing(self):
         # Сохранение истории при закрытии окна
         self.save_history()
         self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing) # Перехват закрытия окна для сохранения истории
    root.mainloop()