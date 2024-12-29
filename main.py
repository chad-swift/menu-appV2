from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QApplication,
    QComboBox,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QPushButton,
    QFrame
)

class MainMenuButton(QPushButton):
    def __init__(self, text):
        super().__init__()

        self.setText(text)
        self.setMinimumSize(150, 50)
        self.setStyleSheet("""
            QPushButton {
                background-color: dimgray;
                color: white;
                border-radius: 10px;
            }
            
            QPushButton:pressed {
                background-color: gray;
            }
        """)


class DayMenu(QWidget):
    def __init__(self, day):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        day_frame = QFrame()
        day_layout = QVBoxLayout()
        day_frame.setFrameShape(QFrame.Box)
        day_frame.setLineWidth(1)
        day_frame.setMinimumSize(200, 150)

        day_label = QLabel(day)
        day_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        day_layout.addWidget(day_label)

        meal_choice_layout = QHBoxLayout()
        meal_choice = QComboBox()
        meal_choice_layout.addWidget(meal_choice)
        meal_choice_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        day_layout.addLayout(meal_choice_layout)


        day_frame.setLayout(day_layout)
        layout.addWidget(day_frame)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Window')

        layout = QHBoxLayout()
        week_layout = QHBoxLayout()
        button_layout = QVBoxLayout()

        days = (
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday',
            'Sunday',
        )

        for day in days:

            day_menu = DayMenu(day)

            week_layout.addWidget(day_menu)

        manage_meals_btn = MainMenuButton('Manage Meals')
        button_layout.addWidget(manage_meals_btn)

        manage_ingredients_btn = MainMenuButton('Manage Ingredients')
        button_layout.addWidget(manage_ingredients_btn)

        export_button = MainMenuButton('Export Menu')
        button_layout.addWidget(export_button)

        layout.addLayout(week_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

main()