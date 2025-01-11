import json

from PySide6.QtWidgets import (
    QPushButton,
    QDialog,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QComboBox,
    QDoubleSpinBox, QFrame, QListWidget, QMessageBox
)

from classes import get_ingredients_from_file, Meal, get_meals_from_file, Ingredient


class AddNewMeal(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Add New Meal")

        self.meal_dialog = parent

        layout = QVBoxLayout()

        frame = QFrame()
        frame.setFrameShape(QFrame.Box)
        frame.setLineWidth(1)
        frame_layout = QVBoxLayout()
        frame.setLayout(frame_layout)

        name_layout = QHBoxLayout()
        name_label = QLabel('Meal Name: ')
        name_layout.addWidget(name_label)
        self.name_edit = QLineEdit()
        name_layout.addWidget(self.name_edit)

        frame_layout.addLayout(name_layout)

        self.meal_ingredients = QListWidget(self)
        frame_layout.addWidget(self.meal_ingredients)

        delete_ingredient = QPushButton('Remove Ingredient from Meal')
        delete_ingredient.clicked.connect(self.remove_ingredient_from_meal)
        frame_layout.addWidget(delete_ingredient)

        ingredient_name_layout = QHBoxLayout()
        ingredient_name_label = QLabel('Ingredient: ')
        ingredient_name_layout.addWidget(ingredient_name_label)
        self.ingredient_choice = QComboBox()
        self.ingredients = self.get_and_update_ingredients()

        ingredient_name_layout.addWidget(self.ingredient_choice)



        quantity_layout = QHBoxLayout()
        quantity_label = QLabel('Quantity: ')
        quantity_layout.addWidget(quantity_label)
        self.quantity = QDoubleSpinBox()
        self.quantity.setMinimum(0)
        self.quantity.setMaximum(500)
        self.quantity.setSingleStep(0.1)
        quantity_layout.addWidget(self.quantity)
        self.quantifier_label = QLabel('Qty')
        self.ingredient_choice.currentIndexChanged.connect(self.update_quantifier_label)
        quantity_layout.addWidget(self.quantifier_label)

        frame_layout.addLayout(ingredient_name_layout)

        frame_layout.addLayout(quantity_layout)

        add_ingredient_button = QPushButton('Add Ingredient to Meal')
        add_ingredient_button.clicked.connect(self.add_ingredient_to_meal)
        frame_layout.addWidget(add_ingredient_button)

        layout.addWidget(frame)

        add_meal_button = QPushButton('Add Meal to Meal List')
        add_meal_button.clicked.connect(self.add_meal_and_close)
        layout.addWidget(add_meal_button)


        self.setLayout(layout)

        self.ingredients_to_add = []

    def get_and_update_ingredients(self):

        ingredients = get_ingredients_from_file()

        for ingredient in ingredients:
            self.ingredient_choice.addItem(ingredient.get_name())
            self.ingredient_choice.setCurrentIndex(-1)

        return ingredients

    def update_quantifier_label(self):
        current_ingredient_index = self.ingredient_choice.currentIndex()

        self.quantifier_label.setText(self.ingredients[current_ingredient_index].get_quantifier())

    def add_ingredient_to_meal(self):

        quantity = self.quantity.value()

        if quantity == 0:
            error_box = QMessageBox()
            error_box.setWindowTitle("Oops!")
            error_box.setText("Ingredients cannot be zero!")
            error_box.exec()
            return

        if self.ingredient_choice.currentIndex() == -1:
            error_box = QMessageBox()
            error_box.setWindowTitle("Oops!")
            error_box.setText("Must pick an ingredient!")
            error_box.exec()
            return

        current_ingredient_index = self.ingredient_choice.currentIndex()

        item_str = f'{self.ingredients[current_ingredient_index].get_name()} {quantity: >10.2f} {self.ingredients[current_ingredient_index].get_quantifier()}'

        self.meal_ingredients.addItem(item_str)
        self.ingredients_to_add.append((self.ingredients[current_ingredient_index], quantity))
        self.ingredient_choice.setCurrentIndex(-1)
        self.quantity.setValue(0)


    def remove_ingredient_from_meal(self):

        current_ingredient_index = self.meal_ingredients.currentRow()

        item = self.meal_ingredients.takeItem(current_ingredient_index)
        if item:
            del item

        self.ingredients_to_add.pop(current_ingredient_index)

    def add_meal_and_close(self):

        meals = get_meals_from_file()

        name = self.name_edit.text()
        ingredients = self.ingredients_to_add

        if not name:
            error_box = QMessageBox()
            error_box.setWindowTitle("Oops!")
            error_box.setText("You need to name your meal!")
            error_box.exec()
            return

        if len(ingredients) == 0:
            error_box = QMessageBox()
            error_box.setWindowTitle("Oops!")
            error_box.setText("You need to add some ingredients!")
            error_box.exec()
            return

        new_meal = Meal(name, ingredients)

        meals.append(new_meal)

        data = {
            'meals': list(map(lambda x: x.to_json(), meals))
        }

        data_json = json.dumps(data, indent=4)

        with open('meals.json', 'w') as file:
            file.write(data_json)

        self.meal_dialog.get_and_update_meals()
        self.close()



