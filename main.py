import sys
import json
import random
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton,
    QListWidget, QVBoxLayout, QWidget, QHBoxLayout, QComboBox,
    QMessageBox
)

class RandomQuoteGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Random Quote Generator")
        self.setGeometry(100, 100, 600, 400)
        self.quotes_file = "quotes.json"
        
        # Загрузка данных
        self.all_quotes = self.load_quotes()
        self.history_quotes = []  # История сгенерированных цитат

        self.init_ui()

    def init_ui(self):
        # Кнопка генерации
        self.generate_btn = QPushButton("Сгенерировать цитату")
        self.generate_btn.clicked.connect(self.generate_quote)

        # Отображение цитаты
        self.quote_label = QLabel("Нажмите кнопку для генерации цитаты")
        self.quote_label.setWordWrap(True)
        self.quote_label.setStyleSheet("font-size: 14px; font-style: italic;")

        # Фильтры
        self.filter_author = QComboBox()
        self.filter_topic = QComboBox()
        self.update_filters()

        self.filter_btn = QPushButton("Фильтровать историю")
        self.filter_btn.clicked.connect(self.filter_history)

        # Список истории
        self.history_list = QListWidget()

        # Layouts
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Автор:"))
        filter_layout.addWidget(self.filter_author)
        filter_layout.addWidget(QLabel("Тема:"))
        filter_layout.addWidget(self.filter_topic)

    def generate_quote(self):
            if not self.all_quotes:
                QMessageBox.information(self, "Информация", "Список цитат пуст. Добавьте новые цитаты в файл.")
                return
            
            quote = random.choice(self.all_quotes)
            self.history_quotes.append(quote)
            self.save_history()
            self.update_history_display(self.history_quotes)
            
            display_text = f'"{quote["text"]}"\n— {quote["author"]} ({quote["topic"]})'
            self.quote_label.setText(display_text)
    
    def update_history_display(self, quotes_list):
            self.history_list.clear()
            for q in quotes_list:
                item_text = f'"{q["text"]}" — {q["author"]} ({q["topic"]})'
                self.history_list.addItem(item_text)
    
    def filter_history(self):
            author = self.filter_author.currentText()
            topic = self.filter_topic.currentText()
            
            filtered = self.history_quotes
            if author != "Все":
                filtered = [q for q in filtered if q["author"] == author]
            if topic != "Все":
                filtered = [q for q in filtered if q["topic"] == topic]
            
            self.update_history_display(filtered)
    
    def update_filters(self):
            authors = set(q["author"] for q in self.all_quotes)
            topics = set(q["topic"] for q in self.all_quotes)
            
            self.filter_author.clear()
            self.filter_topic.clear()
            
            self.filter_author.addItems(["Все"] + sorted(authors))
            self.filter_topic.addItems(["Все"] + sorted(topics))
    
    def load_quotes(self):
            try:
                with open(self.quotes_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                return []
    
    def save_history(self):
            with open("history.json", 'w', encoding='utf-8') as f:
                json.dump(self.history_quotes, f, ensure_ascii=False, indent=4)
    
    def load_history(self):
            try:
                with open("history.json", 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                return []

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RandomQuoteGenerator()
    window.show()
    sys.exit(app.exec())