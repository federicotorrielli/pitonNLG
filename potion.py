class Potion:
    def __init__(self, name, value, ingredients=None):
        if ingredients is None:
            ingredients = []
        self.name = name
        self.value = value
        self.ingredients = ingredients

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    def remove_ingredient(self, ingredient):
        self.ingredients.remove(ingredient)

    def __eq__(self, other):
        return self.name == other.name and self.value == other.value and self.ingredients == other.ingredients

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __hash__(self):
        return hash((self.name, self.value, self.ingredients))

    def __str__(self):
        return f"{self.name} ({self.value}) --> {self.ingredients}"

    def __repr__(self):
        return f"{self.name} ({self.value}) --> {self.ingredients}"

    def get_ingredients(self):
        return self.ingredients

    def set_ingredients(self, ingredients):
        self.ingredients = ingredients

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

    def set_name(self, name):
        self.name = name

    def set_value(self, value):
        self.value = value
