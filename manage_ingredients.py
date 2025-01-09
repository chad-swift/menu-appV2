
from main import *
from classes import *
from PySide6.QtWidgets import (
    QPushButton,
    QDialog,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QFrame,
    QListWidget,
)


class ManageIngredients(QDialog):
    def __init__(self, parent:MainWindow):
        super().__init__(parent)

        self.main_window = parent

        self.setWindowTitle("Manage Ingredients")

        layout = QVBoxLayout()

        ingredient_name_label = QLabel("Ingredients:")
        layout.addWidget(ingredient_name_label)

        self.ingredient_list = QListWidget()

        self.get_and_update_data()

        layout.addWidget(self.ingredient_list)

        delete_ingredient_btn = QPushButton("Delete Ingredient")
        delete_ingredient_btn.clicked.connect(self.remove_ingredient)
        layout.addWidget(delete_ingredient_btn)

        new_ingredient_section_label = QLabel("Add New Ingredient:")
        layout.addWidget(new_ingredient_section_label)

        add_new_ingredient_frame = QFrame()
        add_new_ingredient_frame.setFrameShape(QFrame.Box)
        add_new_ingredient_frame.setLineWidth(1)
        add_new_ingredient_layout = QVBoxLayout()
        add_new_ingredient_frame.setLayout(add_new_ingredient_layout)

        name_row = QHBoxLayout()

        new_ingredient_name_label = QLabel("Ingredient Name:")
        name_row.addWidget(new_ingredient_name_label)

        new_ingredient_name_input = QLineEdit()
        name_row.addWidget(new_ingredient_name_input)

        add_new_ingredient_layout.addLayout(name_row)

        quantifier_row = QHBoxLayout()

        new_ingredient_quantifier_label = QLabel("Ingredient Quantifier:")
        quantifier_row.addWidget(new_ingredient_quantifier_label)
        new_ingredient_quantifier_input = QLineEdit()
        quantifier_row.addWidget(new_ingredient_quantifier_input)
        quantifier_label = QLabel("qty")
        quantifier_row.addWidget(quantifier_label)

        add_new_ingredient_layout.addLayout(quantifier_row)

        add_new_ingredient_button = QPushButton("Add New Ingredient")
        add_new_ingredient_layout.addWidget(add_new_ingredient_button)


        layout.addWidget(add_new_ingredient_frame)


        self.setLayout(layout)

    def get_and_update_data(self):
        ingredients = get_ingredients_from_file()

        for ingredient in ingredients:
            self.ingredient_list.addItem(str(ingredient))

    def remove_ingredient(self):
        current_item = self.ingredient_list.currentItem()
        print(current_item)

    def closeEvent(self, event):
        event.accept()