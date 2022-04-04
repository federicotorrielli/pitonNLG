class Potion:
    def __init__(self, name, ingredients=None):
        if ingredients is None:
            ingredients = {}
        self.name = name
        self.ingredients = ingredients

    def add_ingredient(self, ingredient, quantity):
        self.ingredients[ingredient] = quantity

    def remove_ingredient(self, ingredient):
        self.ingredients.pop(ingredient)

    def __eq__(self, other):
        return self.name == other.name and self.ingredients == other.ingredients

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.name, self.ingredients))

    def __str__(self):
        return f"{self.name} --> {self.ingredients}"

    def __repr__(self):
        return f"{self.name} --> {self.ingredients}"

    def get_ingredients(self):
        return self.ingredients

    def set_ingredients(self, ingredients):
        self.ingredients = ingredients

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_missing_ingredients(self, proposed_ingredients: [str]):
        missing_ingredients = []
        for ingredient in self.ingredients:
            if ingredient not in proposed_ingredients:
                missing_ingredients.append(ingredient)
        return missing_ingredients
