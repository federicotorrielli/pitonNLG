import potion
from fuzzywuzzy import fuzz


class Frame:
    def __init__(self, potion: potion.Potion, ingredients=[]):
        self.potion = potion
        self.ingredients = ingredients
        self.is_complete = False
        self.number_of_operations_made = 0

    def __str__(self):
        return f"{self.potion.name} {self.ingredients}"

    def add_ingredients(self, ingredients):
        if not self.check_complete():
            for ingredient in ingredients:
                for potion_ingredient in self.potion.ingredients:
                    if fuzz.ratio(ingredient, potion_ingredient) > 80:
                        self.ingredients.append(potion_ingredient)
                        break
            self.number_of_operations_made += 1

    def check_complete(self) -> bool:
        if len(self.ingredients) == len(self.potion.ingredients):
            self.is_complete = True
        return self.is_complete
