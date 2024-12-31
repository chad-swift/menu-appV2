from PySide6.QtWidgets import (
    QPushButton,
    QDialog,
    QLabel,
    QListView,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QComboBox,
    QDoubleSpinBox, QFrame
)

class AddNewMeal(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Meal")

        layout = QVBoxLayout()

        frame = QFrame()
        frame.setFrameShape(QFrame.Box)
        frame.setLineWidth(1)
        frame_layout = QVBoxLayout()
        frame.setLayout(frame_layout)

        name_layout = QHBoxLayout()
        name = QLabel('Meal Name: ')
        name_layout.addWidget(name)
        self.name_edit = QLineEdit()
        name_layout.addWidget(self.name_edit)

        frame_layout.addLayout(name_layout)

        self.meal_ingredients = QListView()
        frame_layout.addWidget(self.meal_ingredients)

        delete_ingredient = QPushButton('Delete Meal')
        frame_layout.addWidget(delete_ingredient)

        ingredient_name_layout = QHBoxLayout()
        ingredient_name_label = QLabel('Ingredient: ')
        ingredient_name_layout.addWidget(ingredient_name_label)
        self.ingredient_choice = QComboBox()
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
        quantity_layout.addWidget(self.quantifier_label)

        frame_layout.addLayout(ingredient_name_layout)

        frame_layout.addLayout(quantity_layout)

        add_ingredient_button = QPushButton('Add Ingredient to Meal')
        frame_layout.addWidget(add_ingredient_button)

        layout.addWidget(frame)

        add_meal_button = QPushButton('Add Meal to Meal List')
        layout.addWidget(add_meal_button)


        self.setLayout(layout)
