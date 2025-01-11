from add_new_meal import *
from PySide6.QtWidgets import (
    QPushButton,
    QLabel,
    QListWidget,
    QVBoxLayout,
    QFrame,
    QDialog
)

from classes import get_meals_from_file, get_ingredients_from_file


class ManageMeals(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Manage Meals")

        self.main_window = parent

        layout = QVBoxLayout()

        meal_list_label = QLabel('Meals:')
        layout.addWidget(meal_list_label)

        self.meal_list = QListWidget()
        layout.addWidget(self.meal_list)

        self.meals = self.get_and_update_meals()

        delete_meal_button = QPushButton('Delete Meal')
        delete_meal_button.clicked.connect(self.remove_meal)
        layout.addWidget(delete_meal_button)

        frame = QFrame()
        frame_layout = QVBoxLayout()
        frame.setLayout(frame_layout)
        frame.setFrameShape(QFrame.Box)
        frame.setLineWidth(1)

        add_new_meal_button = QPushButton('Add New Meal')
        add_new_meal_button.clicked.connect(self.__add_new_meal)
        frame_layout.addWidget(add_new_meal_button)

        layout.addWidget(frame)

        self.setLayout(layout)

    def get_and_update_meals(self):
        meals = get_meals_from_file()
        self.meal_list.clear()

        for meal in meals:
            self.meal_list.addItem(meal.get_name())

        return meals

    def remove_meal(self):

        current_meal_index = self.meal_list.currentRow()

        item = self.meal_list.takeItem(current_meal_index)
        if item:
            del item

        self.meals.pop(current_meal_index)

        data = {
            "meals": list(map(lambda meal: meal.to_json(), self.meals))
        }

        data_json = json.dumps(data)

        with open('meals.json', 'w') as file:
            file.write(data_json)


    def __add_new_meal(self):
        dlg = AddNewMeal(self)
        dlg.exec()

    def closeEvent(self, event):
        self.main_window.get_and_update()
