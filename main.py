import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import os
import random
from datetime import datetime

class RandomQuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.history = []
        self.quotes = [
            {"text": "Знание — сила", "author": "Фрэнсис Бэкон", "topic": "Мудрость"},
            {"text": "Быть или не быть — вот в чём вопрос", "author": "Уильям Шекспир", "topic": "Философия"},
            {"text": "Познай самого себя", "author": "Сократ", "topic": "Самопознание"},
            {"text": "Я мыслю, следовательно, существую", "author": "Рене Декарт", "topic": "Философия"},
            {"text": "Через тернии к звёздам", "author": "Сенека", "topic": "Мотивация"}
        ]
        self.load_data()
        self.create_widgets()

    def create_widgets(self):
        # Кнопка генерации цитаты
        tk.Button(self.root, text="Сгенерировать цитату", command=self.generate_quote).pack(pady=10)

        # Отображение текущей цитаты
        self.quote_text = tk.Label(self.root, text="", wraplength=400, justify="center", font=("Arial", 12))
        self.quote_text.pack(pady=5)
        self.author_text = tk.Label(self.root, text="", font=("Arial", 10, "italic"))
        self.author_text.pack(pady=2)
        self.topic_text = tk.Label(self.root, text="", font=("Arial", 9))
        self.topic_text.pack(pady=2)

        # История цитат
        tk.Label(self.root, text="История цитат:").pack(anchor="w", padx=10)
        self.history_list = scrolledtext.ScrolledText(self.root, height=10, width=50)
        self.history_list.pack(padx=10, pady=5, fill="both")

        # Фильтры
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=5)

        tk.Label(filter_frame, text="Фильтр по автору:").grid(row=0, column=0)
        self.author_filter = ttk.Combobox(filter_frame, state="readonly")
        self.author_filter.grid(row=0, column=1, padx=5)
        self.author_filter.bind("<<ComboboxSelected>>", self.apply_filters)

        tk.Label(filter_frame, text="Фильтр по теме:").grid(row=1, column=0)
        self.topic_filter = ttk.Combobox(filter_frame, state="readonly")
        self.topic_filter.grid(row=1, column=1, padx=5)
        self.topic_filter.bind("<<ComboboxSelected>>", self.apply_filters)

         # Кнопки управления
         btn_frame = tk.Frame(self.root)
         btn_frame.pack(pady=10)

         tk.Button(btn_frame, text="Очистить историю", command=self.clear_history).pack(side="left", padx=5)
         tk.Button(btn_frame, text="Сохранить историю", command=self.save_data).pack(side="left", padx=5)

         self.update_filters()

    def generate_quote(self):
         if not self.quotes:
             messagebox.showwarning("Внимание", "Нет доступных цитат!")
             return

         quote = random.choice(self.quotes)
         self.history.append({**quote, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
         self.quote_text.config(text=f'"{quote["text"]}"')
         self.author_text.config(text=f"— {quote['author']}")
         self.topic_text.config(text=f"Тема: {quote['topic']}")
         self.update_history_display()
         self.save_data()

    def update_history_display(self):
         self.history_list.delete(1.0, tk.END)
         for i, quote in enumerate(self.history[-20:], 1):
             self.history_list.insert(tk.END,
                                     f"{i}. \"{quote['text']}\"\n — {quote['author']} ({quote['topic']}) [{quote['timestamp']}]\n\n")

    def update_filters(self):
         authors = sorted(set(q["author"] for q in self.quotes))
         topics = sorted(set(q["topic"] for q in self.quotes))
         self.author_filter["values"] = ["Все"] + authors
         self.topic_filter["values"] = ["Все"] + topics
         self.author_filter.set("Все")
         self.topic_filter.set("Все")

    def apply_filters(self, event=None):
         author_filter = self.author_filter.get()
         topic_filter = self.topic_filter.get()
         filtered = self.quotes

         if author_filter != "Все":
             filtered = [q for q in filtered if q["author"] == author_filter]
         if topic_filter != "Все":
             filtered = [q for q in filtered if q["topic"] == topic_filter]

         if not filtered:
             messagebox.showinfo("Информация", "По заданным фильтрам цитат не найдено")
             return

         quote = random.choice(filtered)
         self.history.append({**quote, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
         self.quote_text.config(text=f'"{quote["text"]}"')
         self.author_text.config(text=f"— {quote['author']}")
         self.topic_text.config(text=f"Тема: {quote['topic']}")
         self.update_history_display()
         self.save_data()

    def clear_history(self):
         self.history = []
         self.update_history_display()

    def save_data(self):
         data = {"quotes": self.quotes, "history": self.history}
         with open("quotes_data.json", "w", encoding="utf-8") as f:
             json.dump(data, f, ensure_ascii=False, indent=4)

    def load_data(self):
         if os.path.exists("quotes_data.json"):
             with open("quotes_data.json", "r", encoding="utf-8") as f:
                 data = json.load(f)
                 self.quotes = data.get("quotes", self.quotes)
                 self.history = data.get("history", [])

if __name__ == "__main__":
     root = tk.Tk()
     app = RandomQuoteGenerator(root)
     root.mainloop()