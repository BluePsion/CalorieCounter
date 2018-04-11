import datetime
from Entry import Entry
import pickle
#Defines a user of the calorie counter program

class User:
    def __init__(self,user_name):
        self.version = "1.0"
        self.user_name = user_name
        self.entries = {} #all entries by user, dictionary with dates for keys, entries for values
        self.weight = 1.0 #all height/weight measurements are imperial
        self.feet = 1
        self.inches = 1
        self.goal_weight = 1.0
        self.calorie_goal = 0
        self.start_date = datetime.date.today()
        self.motd = ""

    def __str__(self):
        return f"{self.user_name} is {self.feet}\'{self.inches} with a current goal weight of {self.goal_weight} pounds and a daily calorie goal of {self.calorie_goal}"
    
#create a test user and save to file, then load it back
if __name__ == "__main__":
    test_user = User("Teste")
    test_user.weight = 210
    test_user.feet = 5
    test_user.inches = 6
    test_user.goal_weight = 180
    test_user.calorie_goal = 2100
    test_user.start_date =  datetime.date.today()
    test_user.MOTD = "Let's do our best!"
    newentry = Entry(datetime.date.today,2100)
    test_user.entries[newentry.entry_date] = newentry
    print("Created test user: ", test_user)
    print("User has", len(test_user.entries), " entries.")

    with open("test.pkl",'wb') as outputfile:
        pickle.dump(test_user,outputfile)
    
    with open("test.pkl",'rb') as infile:
        loaded_user = pickle.load(infile)
    
    print("Loaded back from file", loaded_user)
    print("User has", len(test_user.entries), "entries.")



    

        