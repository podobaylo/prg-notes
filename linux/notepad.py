#!/usr/bin/env python3
# редактор заметок на QT
import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QPushButton, QVBoxLayout, QInputDialog, QMessageBox
from PyQt5.QtCore import Qt

wrkfile = "notes-mj.txt"

class Widget(QWidget):

    def __init__(self):
        super().__init__()
        self.label = QLabel("My Notepad")
        self.textbox = QTextEdit()
        self.button = QPushButton("Save")
        self.layout = QVBoxLayout()
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.textbox)
        self.layout.addWidget(self.button)
        
        self.setLayout(self.layout)
        
        self.button.clicked.connect(lambda: self.save_file(wrkfile))

        # Переменная для хранения последнего поискового запроса
        self.last_search_text = ""

        # Загружаем содержимое файла в текстовое поле
        if os.path.exists(wrkfile):
            with open(wrkfile, "r") as f:
                self.textbox.setText(f.read())
        else:
            with open(wrkfile, "w") as f:
                f.write("[My Notes]")

    def save_file(self, filename):
        with open(filename, "w") as f:
            f.write(self.textbox.toPlainText())
        self.label.setText("File saved successfully!")

    def keyPressEvent(self, event):
        # Обрабатываем комбинацию клавиш Ctrl+F для поиска
        if event.key() == Qt.Key_F and event.modifiers() == Qt.ControlModifier:
            self.open_search_dialog()
        else:
            super().keyPressEvent(event)  # Передаем остальные события родительскому классу

    def open_search_dialog(self):
        # Используем последний поисковый запрос по умолчанию
        search_text, ok = QInputDialog.getText(self, 'Search', 'Enter text to search:', text=self.last_search_text)
        
        if ok and search_text:
            self.last_search_text = search_text  # Сохраняем текущий поисковый запрос
            self.search_text(search_text)

    def search_text(self, text):
        cursor = self.textbox.textCursor()
        
        # Сбрасываем курсор в начало текста
        cursor.movePosition(cursor.Start)

        found = False
        while True:
            if not self.textbox.find(text):  # Используем метод find() QTextEdit
                break  # Если текст не найден, выходим из цикла
            found = True
            
            # Устанавливаем курсор для выделения найденного текста
            cursor = self.textbox.textCursor()  # Получаем текущий курсор
            cursor.movePosition(cursor.StartOfBlock)  # Возвращаемся к началу блока
            cursor.movePosition(cursor.EndOfBlock, cursor.KeepAnchor)  # Выделяем весь блок текста
            
            # Устанавливаем курсор для выделения найденного текста
            self.textbox.setTextCursor(cursor)
            break  # Выход из цикла после первого нахождения

        if not found:
            QMessageBox.information(self, "Search", f"'{text}' not found.")

app = QApplication(sys.argv)
widget = Widget()
widget.resize(800, 600)
widget.show()
sys.exit(app.exec_())
