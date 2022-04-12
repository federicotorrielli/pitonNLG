import potion


class Frame:
    def __init__(self, frame_potion: potion.Potion, ingredients=None):
        if ingredients is None:
            ingredients = []
        self.potion = frame_potion
        self.ingredients = set(ingredients)
        self.error_ingredients = set([])
        self.external_ingredients = set([])
        self.is_complete = False
        self.is_correct = False
        self.number_of_operations_made = 0

    def __str__(self) -> str:
        return f"{self.potion.name} {self.ingredients}"

    def debug(self):
        print(f"Frame name:{self.potion.name}= [{self.ingredients}]")
        print(f"Potion Ingredients: {self.potion.ingredients}")
        print(f"Errors: {self.error_ingredients}")
        print(f"External Ingredients: {self.external_ingredients}")
        print(f"Is complete: {self.is_complete}" + str(len(self.ingredients) + len(self.error_ingredients)) + "==" + str(len(self.potion.ingredients)))
        print(f"Is correct: {self.is_correct}")
        print(f"Number of op made: {self.number_of_operations_made}")

    def add_ingredients(self, ingredients: set, positive: [bool]):
        if not self.check_complete():
            for count, ingredient in enumerate(ingredients):
                if ingredient in self.potion.ingredients:
                    if positive[count]:
                        self.ingredients.add(ingredient)
                    else:
                        self.error_ingredients.add(ingredient)
                else:
                    if positive[count]:
                        self.external_ingredients.add(ingredient)
            self.number_of_operations_made += 1

    def check_complete(self) -> bool:
        if len(self.ingredients) + len(self.error_ingredients) == len(self.potion.ingredients):
            self.is_complete = True
        return self.is_complete
