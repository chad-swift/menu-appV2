from PySide6.QtWidgets import (
    QPushButton,
    QDialog,
    QLabel,
    QListView,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QFrame,
    QDialog
)

class ManageMeals(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manage Meals")

        layout = QVBoxLayout()

        meal_list_label = QLabel('Meals:')
        layout.addWidget(meal_list_label)

        self.meal_list = QListView()
        layout.addWidget(self.meal_list)

        delete_meal_button = QPushButton('Delete Meal')
        layout.addWidget(delete_meal_button)

        frame = QFrame()
        frame_layout = QVBoxLayout()
        frame.setLayout(frame_layout)
        frame.setFrameShape(QFrame.Box)
        frame.setLineWidth(1)

        add_new_meal_button = QPushButton('Add New Meal')
        frame_layout.addWidget(add_new_meal_button)

        layout.addWidget(frame)

        self.setLayout(layout)
