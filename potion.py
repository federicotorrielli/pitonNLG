class Potion:
    def __init__(self, name, ingredients=None):
        if ingredients is None:
            ingredients = []
        self.name = name.lower()
        self.ingredients = [ingredient.lower() for ingredient in ingredients]

    def add_ingredient(self, ingredient: str):
        self.ingredients.append(ingredient)

    def remove_ingredient(self, ingredient: str):
        self.ingredients.remove(ingredient)

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

    def get_ingredients(self) -> [str]:
        return self.ingredients

    def set_ingredients(self, ingredients: [str]):
        self.ingredients = ingredients

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str):
        self.name = name
