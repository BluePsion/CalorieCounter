#git test
import pickle
import sys
import datetime
import os
from User import User
from Entry import Entry
from Food import Food
#cc.py (Calorie Counter)
#Counts calories and keeps track of calorie/weight goals
#BluePsion - 2018

def clear_screen():
    os.system('cls')

def save_user(user):
    with open((user.user_name + ".pkl"),'wb') as outfile:
        pickle.dump(user,outfile)

def load_user(user_name):
    try:
        with open(user_name + ".pkl",'rb') as infile:
            user = pickle.load(infile)
    except Exception as ex:
        print("Unable to load profile ", user_name, "file. Error: ", ex, ex.with_traceback)
        user = None
    
    return user

def check_for_entry(date_to_load):
    if not (loaded_date in user.entries):
        user.entries[loaded_date] = Entry(loaded_date,user.calorie_goal)

def edit_journal(journal):
    while(True):
        print("Today's Entry: ")
        print(journal)
        print("\n\n\n")
        print("1. Add to entry")
        print("2. Delete a line")
        print("3. Clear journal entry")
        print("4. Back")
        print("\n")
        choice = input("Your choice: ")
    
        if(choice == "1"):
            print("Enter in \"x\" alone to exit.")
            while(True):
                newline = input(": ")
                if(newline=="x"): 
                    break
                else: journal = journal + (newline + "\n")
        
        if(choice == "2"):
            pass
        
        if(choice == "3"):
            confirm = input("You sure you want to delete today's Entry? \"y\" to confirm: ")
            if(confirm == "y"): journal = ""
        
        if(choice == "4"):
            return journal

#Traps user until they give us a damn float
def get_pos_float_from_user(prompt):
    while(True):
        try:
            i = float(input(prompt))
            if i <= 0 : raise ValueError
            break
        except ValueError:
            print("Please enter in a positive number.")
    return i

def get_pos_int_from_user(prompt):
    while(True):
        try:
            i = input(prompt)
            i = int(i)
            if i <= 0 : raise ValueError
            break
        except ValueError:
            print("Please enter in a positive number.")
    return i



def settings_menu(user):
    while(True):
        print("\n\n\n")
        print("1. Edit Goals")
        print("2. Edit MOTD")
        print("3. Change/Load Profile")
        print("4. Back")
        print("\n")
        choice = input("Your choice: ")
        if(choice == "1"):
            user.goal_weight = get_pos_float_from_user("What is your goal weight?: ")
            print("\n")
            user.calorie_goal = get_pos_int_from_user("What is your daily calorie goal? ")
        elif(choice == "2"):
            print("\n")
            user.motd = input("Enter new MOTD: ")
        elif(choice == "3"):
            print("\n")
            user_name = input("Enter in user name or new for a new user: ")
            if(user_name == "new"):
                print("Hello! Let's get you set up <3!")
                print("\n")
                new_name = input("Enter your name: ")
                newuser = User(new_name)
                print("Now to find out how tall you are")
                newuser.feet = get_pos_int_from_user("How tall are you (feet): ")
                newuser.inches = get_pos_int_from_user("How tall are you (inches): ")
                print("\n")
                newuser.weight = get_pos_float_from_user("How much do you weigh:  ")
                newuser.goal_weight = get_pos_float_from_user("What is your goal weight?: ")
                print("\n")
                newuser.calorie_goal = get_pos_int_from_user("What is your daily calorie goal?: ")
                print("\n")
                newuser.motd = input("MOTD (Displayed on main menu): ")
                print("\n")
                print("Thanks, I'll save all that and you are ready to go!")
                user = newuser
            else:
                olduser = user
                user = load_user(user_name)
                if user == None:
                    user = olduser
        elif(choice == "4"):
            break
    return user

def view_food_list(foodlist):
        while(True):
            print("\n")
            print("\n")
            print("\n")
            print("Your food today-----------------------------")
            display_list(foodlist)
            print("--------------------------------------------")
            print("1. Remove one food.")
            print("2. Clear today's list.")
            print("3. Back")
            print("\n")
            choice = input("Your choice: ")

            if(choice == "1"):
                removechoice = input("Which entry would you like to remove.")
                try:
                    del foodlist[int(removechoice)-1]
                    print("Removed entry.")
                except IndexError:
                    print("No entry at that number.")
            if(choice == "2"):
                foodlist = []
                print("Food list cleared.")
            if(choice == "3"):
                break
        #return foodlist
                

def display_dict(dict):
        if(len(dict) > 0):
            for i in dict:
                print ((i), " ", dict[i])
        else:
            print("Nothing here yet.")

def display_list(list):
    if (len(list) > 0):
            for i in range(len(list)):
                print((i+1), list[i])
    else:
        print("Nothing here.")

user = User(", please create your profile!")
settings = {}

#Load the default user if possible
try:
    with open("settings.pkl",'rb') as infile:
        settings = pickle.load(infile)
        user = load_user(settings["default_profile"])
        if user == None:
            user = User(", please create your profile!")
except Exception as ex:
        print("No default profile found. ")

#Load entry for today
loaded_date = datetime.date.today()
check_for_entry(loaded_date)

while(True):
    save_user(user) #auto-save ;)
    check_for_entry(loaded_date)
    print("\n")
    print("\n")
    print("\n")
    print(f"Welcome {user.user_name}!")
    print ("< ",loaded_date.strftime("%A the %d of %B, %Y")," >")
    print ("Calorie goal: ", user.calorie_goal)
    print ("Calories left: ", int(user.calorie_goal) - user.entries[loaded_date].total_calories() )
    print ("You are ", int(user.weight) - int(user.goal_weight) , " pounds from your goal weight!")
    #print ("Journal Entry: \n", user.entries[loaded_date].journal)
    print(f"***{user.motd}***")
    print("1. Weigh-In")
    print("2. List food so far today")
    print("3. Journal")
    print("4. Settings")
    print("5. Exit")
    print("--------------------------------------------")
    print("\n")
    choice  = input("Enter in food name or option: ") # < will go back a day and > forward
    if(choice == "1"):
        print("Brave enough to get on a scale huh?")
        user.weight = get_pos_float_from_user("What is your weight now: ")
    elif(choice == "3"):
        user.entries[loaded_date].journal = edit_journal(user.entries[loaded_date].journal)
    elif(choice == "2"):
        view_food_list(user.entries[loaded_date].food)
    elif(choice == "4"):
        user = settings_menu(user)
    elif(choice == "5"): 
        #we want to load the current user as default for next load
        settings["default_profile"] = user.user_name
        with open("settings.pkl","wb") as outfile:
            pickle.dump(settings,outfile)
        sys.exit()
    elif(choice == "<"):
        loaded_date = loaded_date - datetime.timedelta(days=1)
    elif(choice == ">"):
        loaded_date = loaded_date + datetime.timedelta(days=1)

    else:
        #TODO check for number
        calories = get_pos_int_from_user("How many calories?: ")
        user.entries[loaded_date].food.append(Food(choice, calories))
    



