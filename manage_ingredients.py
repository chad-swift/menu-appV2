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
    QMessageBox
)


class ManageIngredients(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.main_window = parent

        self.setWindowTitle("Manage Ingredients")

        layout = QVBoxLayout()

        ingredient_name_label = QLabel("Ingredients:")
        layout.addWidget(ingredient_name_label)

        self.ingredient_list = QListWidget()

        self.get_and_update_ingredients()

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

        self.new_ingredient_name_input = QLineEdit()
        name_row.addWidget(self.new_ingredient_name_input)

        add_new_ingredient_layout.addLayout(name_row)

        quantifier_row = QHBoxLayout()

        new_ingredient_quantifier_label = QLabel("Ingredient Quantifier:")
        quantifier_row.addWidget(new_ingredient_quantifier_label)
        self.new_ingredient_quantifier_input = QLineEdit()
        quantifier_row.addWidget(self.new_ingredient_quantifier_input)
        examples_label = QLabel("(oz, lbs, slc, etc.)")
        quantifier_row.addWidget(examples_label)

        add_new_ingredient_layout.addLayout(quantifier_row)

        add_new_ingredient_button = QPushButton("Add New Ingredient")
        add_new_ingredient_button.clicked.connect(self.add_ingredient)
        add_new_ingredient_layout.addWidget(add_new_ingredient_button)


        layout.addWidget(add_new_ingredient_frame)


        self.setLayout(layout)

    def get_and_update_ingredients(self):
        ingredients = get_ingredients_from_file()

        for ingredient in ingredients:
            self.ingredient_list.addItem(str(ingredient))

    def add_ingredient(self):
        name = self.new_ingredient_name_input.text()
        quantifier = self.new_ingredient_quantifier_input.text()

        if not name or not quantifier:
            error_box = QMessageBox()
            error_box.setWindowTitle("Uh Oh")
            error_box.setText("Ingredient and Quantifier should both be filled out")
            error_box.exec()
            return


        if quantifier.isnumeric():
            error_box = QMessageBox()
            error_box.setWindowTitle("Uh Oh")
            error_box.setText("Quantifier should be a string!")
            error_box.exec()
            return

        if name.isnumeric():
            error_box = QMessageBox()
            error_box.setWindowTitle("Uh Oh")
            error_box.setText("Name should be a string!")
            error_box.exec()
            return

        new_ingredient = Ingredient(name, quantifier)
        self.ingredient_list.addItem(str(new_ingredient))

        data = get_ingredients_from_file()
        data.append(new_ingredient)

        data_object = {
            "ingredients": list(map(lambda ingredient: ingredient.to_json(), data)),
        }

        data_json = json.dumps(data_object, indent=4)

        with open('ingredients.json', 'w') as outfile:
            outfile.write(data_json)



    def remove_ingredient(self):

        data = get_ingredients_from_file()

        current_item_index = self.ingredient_list.currentIndex().row()

        item = self.ingredient_list.takeItem(current_item_index)
        if item:
            del item

        data.pop(current_item_index)

        data_object = {
            "ingredients": list(map(lambda ingredient: ingredient.to_json(), data))
        }

        data_json = json.dumps(data_object, indent=4)

        with open('ingredients.json', 'w') as outfile:
            outfile.write(data_json)



    def closeEvent(self, event):
        self.main_window.get_and_update()
        event.accept()