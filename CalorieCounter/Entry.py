from datetime import date
from Food import Food
#Defines a day of food for use in a calorie counter
class Entry():
    def __init__(self, entry_date, calorie_goal):
        self.entry_date = entry_date
        self.food = []
        self.calorie_goal = calorie_goal
        self.journal = ""
    
    def __str__(self):
        return("Entry created: ", self.entry_date, " with goal of ", self.calorie_goal, " calories.")

    def total_calories(self):
        total = 0
        if(len(self.food) > 0):
            for f in self.food:
                total = total + int(f.calories)
        return total
                




    

