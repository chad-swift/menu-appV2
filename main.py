import sys
from manage_ingredients import *
from manage_meals import *
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
                border-radius: 15px;
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
        self.meal_choice = QComboBox()
        meal_choice_layout.addWidget(self.meal_choice)
        meal_choice_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        day_layout.addLayout(meal_choice_layout)


        day_frame.setLayout(day_layout)
        layout.addWidget(day_frame)

        self.setLayout(layout)

    def get_combobox(self):
        return self.meal_choice

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

        self.combo_boxes = []

        for day in days:

            day_menu = DayMenu(day)

            self.combo_boxes.append(day_menu.get_combobox())

            week_layout.addWidget(day_menu)

        self.get_and_update()

        manage_meals_btn = MainMenuButton('Manage Meals')
        button_layout.addWidget(manage_meals_btn)
        manage_meals_btn.clicked.connect(self.__open_manage_meals_dialog)

        manage_ingredients_btn = MainMenuButton('Manage Ingredients')
        button_layout.addWidget(manage_ingredients_btn)
        manage_ingredients_btn.clicked.connect(self.__open_manage_ingredients_dialog)

        export_button = MainMenuButton('Export Menu')
        button_layout.addWidget(export_button)
        export_button.clicked.connect(self.create_menu_list)

        layout.addLayout(week_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def get_and_update(self):
        meals = get_meals_from_file()

        for combobox in self.combo_boxes:
            combobox.clear()
            combobox.addItems(list(map(lambda meal: meal.get_name(), meals)))

    def create_menu_list(self):
        meals = get_meals_from_file()
        ingredients = get_ingredients_from_file()

        meals_for_the_week = []

        for meal in self.combo_boxes:
            meals_for_the_week.append(meal.currentText())

        ingredient_list: list[str] = []
        meal_list: list[Meal] = []

        for meal_name in meals_for_the_week:
            for meal in meals:
                if meal.get_name() == meal_name:
                    meal_list.append(meal)

        for ingredient in ingredients:
            quantity = 0
            ingredient_name = ''
            quantifier = 'qty'
            for meal in meal_list:
                ingredient_name = ingredient.get_name()
                meal_ingredients = meal.get_ingredient_names()
                if ingredient_name not in meal_ingredients:
                    continue
                quantity += meal.get_specific_ingredient_quantity(ingredient_name)
                quantifier = meal.get_specific_ingredient_quantifier(ingredient_name)
            if quantity == 0:
                continue
            ingredient_list.append(f'{quantity:.2f} {quantifier} of {ingredient_name}')


        with open('menu.txt', 'w') as f:
            i = 0

            days = (
                'Monday',
                'Tuesday',
                'Wednesday',
                'Thursday',
                'Friday',
                'Saturday',
                'Sunday'
            )

            f.write('Menu:\n----------------\n')
            for meal_name in meals_for_the_week:
                f.write(f'{days[i]}: {meal_name} \n')
                i += 1
            f.write(f'\nIngredients Needed for Meals selected:\n-----------------\n')
            for ingredient in ingredient_list:
                f.write(ingredient + '\n')
        success_box = QMessageBox()
        success_box.setWindowTitle('Success')
        success_box.setText('Successfully Exported Menu')
        success_box.exec()



    def __open_manage_ingredients_dialog(self):

        dlg = ManageIngredients(self)
        dlg.exec()


    def __open_manage_meals_dialog(self):
        dlg = ManageMeals(self)
        dlg.exec()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

main()