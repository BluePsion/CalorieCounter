#defines a piece of food

class Food():
    def __init__(self, name, calories):
        self.name = name
        self.calories = calories

    def __str__(self):
        return f"{self.name} : {self.calories}"