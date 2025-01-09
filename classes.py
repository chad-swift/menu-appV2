import json

class Ingredient:
    """
    Class used to create an Ingredient for a Meal.
    Parameters: Name - Name of the meal, Quantifier - how that ingredient should be quantified (example: oz, lbs)
    """
    def __init__(self, name: str, quantifier: str):
        self.name = name
        self.quantifier = quantifier
    
    def get_name(self):
        """
        Returns the Ingredient name
        """
        return self.name
    
    def set_name(self, new_name: str):
        """
        Replaces the Ingredient name with a new name
        """
        self.name = new_name

    def get_quantifier(self):
        """
        Gets the ingredient quantifier
        """
        return self.quantifier

    def set_quantifier(self, new_quantifier):
        """
        Replaces the ingredient quantifier with a new quantifier
        """
        self.quantifier = new_quantifier

    def __str__(self):
        """
        Nice formatting to be able to print an ingredient in a string format in things like listboxes
        """
        return f'{self.name: <25}...{self.quantifier: >10}'

    def to_json(self):
        return {"name": self.name, "quantifier": self.quantifier}

class Meal:
    """
    Class that creates a meal from a name and a list tuples that define the ingredient and how much of that ingredient
    """
    def __init__(self, name: str, ingredients: list[tuple[Ingredient, float]]):
        self.name = name
        self.ingredients = ingredients

        # This got a little complicated, but we need to take in a list of tuples so that the number of a specific ingredient stays with that ingredient
        self.ingredient_list = {}

        # we can then save all the information passed to the class in a dict, which makes it easy to access everything later
        for ingredient, quantity in self.ingredients:
            self.ingredient_list[ingredient.get_name()] = {
                "ingredient": ingredient,
                "quantity": quantity
            }

    def get_name(self):
        """
        returns the name of the Meal
        """
        return self.name
    
    def set_name(self, new_name):
        """
        replaces the name of the Meal with a new name
        """

        self.name = new_name

    def get_ingredients(self):
        """
        Returns the list of Ingredients from the Meal
        """
        ingredients = []

        for _, value in self.ingredient_list.items():
            ingredients.append(value['ingredient'])

        return ingredients

    def get_ingredient_names(self):
        """
        returns only the names of the ingredients
        """
        names = []

        for key, value in self.ingredient_list.items():
            names.append(key)

        return names
    
    def get_ingredient_quantities(self):
        quantities = []

        for key, value in self.ingredient_list.items():
            quantities.append((key, value['quantity']))

        return quantities
    
    def get_specific_ingredient_quantity(self, ingredient_name):
        """
        Returns the quantity of a specific ingredient found in a Meal given its name
        """
        return self.ingredient_list[ingredient_name]['quantity']
    
    def set_specific_ingredient_quantity(self, ingredient_name, new_quantity):
        """
        Replaces the quantity of a specific ingredient found in a Meal given its name
        """
        self.ingredient_list[ingredient_name]['quantity'] = new_quantity

    def get_specific_ingredient_quantifier(self, ingredient_name: str):
        """
        Returns a quantifier of a specific meal given its name
        """
        return self.ingredient_list[ingredient_name]['ingredient'].get_quantifier()
    
    def append_ingredient(self, ingredient: Ingredient, quantity):
        """
        Adds a new ingredient to a meal
        """
        self.ingredient_list[ingredient.get_name()] = {
            "ingredient": ingredient,
            "quantity": quantity
        }

    def to_json(self):
        ingredients = self.get_ingredients()
        return {
            "name": self.name,
            "ingredients": list(map(lambda ingredient:
                                       {"name": ingredient.get_name(),
                                        "quantifier": ingredient.get_quantifier(),
                                        "quantity": self.get_specific_ingredient_quantity(ingredient.get_name())
                                        }, ingredients))}


def get_meals_from_file():
    meals = []

    with open('meals.json', 'r') as infile:
        meals_data = json.load(infile)

    for entry in meals_data['meals']:
        meal = Meal(entry['name'],
                    list(map(lambda x: (Ingredient(x['name'], x['quantifier']), x['quantity']), entry['ingredients'])))
        meals.append(meal)

    return meals

def get_ingredients_from_file():
    ingredients = []

    with open('ingredients.json', 'r') as infile:
        ingredients_data = json.load(infile)

    for entry in ingredients_data['ingredients']:
        ingredient = Ingredient(entry['name'], entry['quantifier'])
        ingredients.append(ingredient)

    return ingredients
