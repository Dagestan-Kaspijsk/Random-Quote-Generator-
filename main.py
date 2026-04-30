import sys
import json
import random
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QListWidget,
    QVBoxLayout, QWidget, QHBoxLayout, QComboBox, QMessageBox
)

class RandomQuoteGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Random Quote Generator")
        self.setGeometry(100, 100, 600, 450)
        self.quotes_file = "quotes.json"
        self.history_file = "history.json"

        # Загрузка данных
        self.all_quotes = self.load_quotes()
        self.history_quotes = self.load_history()

        self.init_ui()
        self.update_history_display(self.history_quotes)
        self.update_filters()

    def init_ui(self):
        # Центральный widget и основной layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Кнопка генерации и отображение цитаты
        self.generate_btn = QPushButton("Сгенерировать цитату")
        self.generate_btn.clicked.connect(self.generate_quote)
        
        self.quote_label = QLabel("Нажмите кнопку для генерации цитаты")
        self.quote_label.setWordWrap(True)
        self.quote_label.setStyleSheet("font-size: 14px; font-style: italic; padding: 10px;")

        # Фильтры
        filter_layout = QHBoxLayout()
        self.filter_author = QComboBox()
        self.filter_topic = QComboBox()
        self.filter_btn = QPushButton("Фильтровать историю")
        self.filter_btn.clicked.connect(self.filter_history)
        
        filter_layout.addWidget(QLabel("Автор:"))
        filter_layout.addWidget(self.filter_author)
        filter_layout.addWidget(QLabel("Тема:"))
        filter_layout.addWidget(self.filter_topic)
        filter_layout.addWidget(self.filter_btn)

        # Список истории
        self.history_list = QListWidget()

        # Добавление всех элементов в главный layout
        main_layout.addWidget(self.quote_label)
        main_layout.addWidget(self.generate_btn)
        main_layout.addLayout(filter_layout)
        main_layout.addWidget(self.history_list)

    def generate_quote(self):
        if not self.all_quotes:
            QMessageBox.information(self, "Информация", "Список цитат пуст. Добавьте новые цитаты в файл.")
            return

        quote = random.choice(self.all_quotes)
        
        # Проверка структуры цитаты
        if not all(key in quote for key in ["text", "author", "topic"]):
            QMessageBox.critical(self, "Ошибка данных", "Некорректная структура цитаты в файле.")
            return

        self.history_quotes.append(quote)
        self.save_history()
        self.update_history_display(self.history_quotes)
        
        display_text = f'"{quote["text"]}"\n— {quote["author"]} ({quote["topic"]})'
        self.quote_label.setText(display_text)

    def update_history_display(self, quotes_list):
        self.history_list.clear()
        for q in quotes_list:
            if not all(key in q for key in ["text", "author", "topic"]):
                continue  # Пропускаем некорректные записи
            item_text = f'"{q["text"]}" — {q["author"]} ({q["topic"]})'
            self.history_list.addItem(item_text)

    def filter_history(self):
        author = self.filter_author.currentText()
        topic = self.filter_topic.currentText()
        
        filtered = self.history_quotes.copy()
        
        if author != "Все":
            filtered = [q for q in filtered if q.get("author") == author]
        if topic != "Все":
            filtered = [q for q in filtered if q.get("topic") == topic]
        
        self.update_history_display(filtered)

    def update_filters(self):
        authors = set(q.get("author", "") for q in self.all_quotes if "author" in q)
        topics = set(q.get("topic", "") for q in self.all_quotes if "topic" in q)
        
        self.filter_author.clear()
        self.filter_topic.clear()
        
        self.filter_author.addItems(["Все"] + sorted(authors))
        self.filter_topic.addItems(["Все"] + sorted(topics))

    def load_quotes(self):
        try:
            with open(self.quotes_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list) and all(isinstance(x, dict) for x in data):
                    return data
                else:
                    QMessageBox.warning(self, "Предупреждение", "Некорректный формат quotes.json. Будет использован пустой список.")
                    return []
                    return []
        except (FileNotFoundError, json.JSONDecodeError) as e:
            QMessageBox.warning(self, "Предупреждение", f"Не удалось загрузить quotes.json: {e}. Будет использован пустой список.")
            return []

    def load_history(self):
         try:
             with open(self.history_file, 'r', encoding='utf-8') as f:
                 data = json.load(f)
                 if isinstance(data, list) and all(isinstance(x, dict) for x in data):
                     return data
                 else:
                     return []
         except (FileNotFoundError, json.JSONDecodeError):
             return []
 
    def save_history(self):
         try:
             with open(self.history_file, 'w', encoding='utf-8') as f:
                 json.dump(self.history_quotes, f, ensure_ascii=False, indent=4)
         except Exception as e:
             QMessageBox.critical(self, "Ошибка сохранения", f"Не удалось сохранить историю: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RandomQuoteGenerator()
    window.show()
    sys.exit(app.exec())