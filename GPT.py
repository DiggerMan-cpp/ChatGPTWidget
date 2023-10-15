import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QPushButton, QVBoxLayout, QTextEdit, QLabel
import openai

class DesktopWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Desktop Widget')
        self.setGeometry(100, 100, 400, 300)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint | Qt.Tool | Qt.SplashScreen)
        self.setWindowOpacity(0.7)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(palette.Window, QColor(0, 0, 0))
        self.setPalette(palette)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.api_key_input = self.create_text_input("Введите ваш API ключ")
        layout.addWidget(self.api_key_input)

        self.input_field = self.create_text_input()
        layout.addWidget(self.input_field)

        self.send_button = self.create_button('Отправить', self.send_message)
        layout.addWidget(self.send_button)

        self.label = self.create_text_output()
        layout.addWidget(self.label)

        self.resize_button = self.create_button('Увеличить', self.toggle_window_size)
        layout.addWidget(self.resize_button)

        self.central_widget.setLayout(layout)
        self.dragging = False
        self.oldPos = None
        self.is_maximized = False

    def create_text_input(self, placeholder_text=""):
        text_input = QLineEdit(self)
        text_input.setPlaceholderText(placeholder_text)
        return text_input

    def create_text_output(self):
        text_output = QTextEdit(self)
        text_output.setFont(QFont("Arial", 12))
        text_output.setReadOnly(True)
        return text_output

    def create_button(self, text, function):
        button = QPushButton(text)
        button.clicked.connect(function)
        return button

    def mousePressEvent(self, event):
        if self.api_key_input.geometry().contains(event.pos()):
            return
        self.dragging = True
        self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.dragging = False

    def mouseMoveEvent(self, event):
        if self.dragging:
            delta = event.globalPos() - self.oldPos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def send_message(self):
        user_input = self.input_field.text()
        api_key = self.api_key_input.text()

        if user_input and api_key:
            openai.api_key = api_key

            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=user_input,
                max_tokens=50
            )

            self.label.setText(response.choices[0].text)

    def toggle_window_size(self):
        if self.is_maximized:
            self.setGeometry(100, 100, 400, 300)
            self.is_maximized = False
        else:
            self.setGeometry(self.x(), self.y(), self.width() * 2, self.height() * 2)
            self.is_maximized = True

def main():
    app = QApplication(sys.argv)
    widget = DesktopWidget()
    widget.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
