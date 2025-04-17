import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from functools import partial

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculator")
        self.setGeometry(100, 100, 300, 450)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.history_label = QLabel("History:")
        self.layout.addWidget(self.history_label)
        self.test_operation = 0 #tester si il y a une opération à été déjà faite

        self.result_display = QLineEdit()
        self.result_display.setAlignment(Qt.AlignRight)
        self.result_display.setStyleSheet(
            "QLineEdit {"
            "   background-color: #f0f0f0;"
            "   border: 1px solid #d0d0d0;"
            "   font-size: 24px;"
            "   padding: 5px;"
            "}"
        )
        self.layout.addWidget(self.result_display)

        self.create_buttons()

    def create_buttons(self):
        button_layout = QVBoxLayout()
        button_rows = [
            ("7", "8", "9", "/"),
            ("4", "5", "6", "x"),
            ("1", "2", "3", "-"),
            ("0", ".", "=", "+")
        ]

        for row in button_rows:
            row_layout = QHBoxLayout()
            for text in row:
                button = QPushButton(text)
                if text == "=":
                    button.clicked.connect(self.equal_clicked)
                else:
                    button.clicked.connect(partial(self.button_clicked, text))
                button.setStyleSheet(
                    "QPushButton {"
                    "   background-color: #f0f0f0;"
                    "   border: 1px solid #d0d0d0;"
                    "   font-size: 20px;"
                    "   width: 60px;"
                    "   height: 60px;"
                    "}"
                    "QPushButton:hover {"
                    "   background-color: #e0e0e0;"
                    "}"
                    "QPushButton:pressed {"
                    "   background-color: #c0c0c0;"
                    "}"
                )
                row_layout.addWidget(button)
            button_layout.addLayout(row_layout)

        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_clicked)
        clear_button.setStyleSheet(
            "QPushButton {"
            "   background-color: #ff6666;"
            "   border: 1px solid #ff4d4d;"
            "   color: white;"
            "   font-size: 20px;"
            "   width: 60px;"
            "   height: 60px;"
            "}"
            "QPushButton:hover {"
            "   background-color: #ff4d4d;"
            "}"
            "QPushButton:pressed {"
            "   background-color: #ff3333;"
            "}"
        )
        button_layout.addWidget(clear_button)

        self.layout.addLayout(button_layout)

    def button_clicked(self, text):
        if text == 'x':
            self.result_display.setText(self.result_display.text() + '*')#Pour que ça affiche * au lieu de x comme opérateur
        else:
            #améliorer un peu
            if self.test_operation == 1 and (text != '+' or text != '-' or text!='/'):
                self.result_display.setText(text)
                self.test_operation = 0
            else:
                self.result_display.setText(self.result_display.text() + text)


    def equal_clicked(self):
        expression = self.result_display.text()
        last_history = ''
        try:
            result = eval(expression)
            self.result_display.setText(str(result))
            last_history = self.history_label.setText(f"History: {last_history}\n {expression}   =   {result}")
            self.test_operation = 1

        except Exception as e:
            self.result_display.setText("Error")

    def clear_clicked(self):
        self.result_display.clear()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Return or key == Qt.Key_Enter:
            self.equal_clicked()
        elif key == Qt.Key_Escape:
            self.clear_clicked()
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec_())
