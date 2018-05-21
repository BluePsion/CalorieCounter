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
version = "1.0"
def get_timestamp():
    return datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

def clear_screen():
    os.system('cls')

def save_user(user):
    with open((user.user_name + ".pkl"),'wb') as outfile:
        pickle.dump(user,outfile)

def load_user(user_name):
    user = None
    try:
        with open(user_name + ".pkl",'rb') as infile:
            user = pickle.load(infile)
    except Exception as ex:
        print("Unable to load profile ", user_name, "file. Error: ", ex, ex.with_traceback)
        user = None
    if not(user==None):
        user = update_profile(user) 
    return user

def update_profile(user):
    current = False
    try:
        current = (user.version == version)       
    except AttributeError:
        #no version on user meaning made before versions implemented
        user.version = "BETA"
        current = False
    if not current:
        print("User profile has version ", user.version, " now updating profile to current version (" + version + ").")
        user = update_user(user)
        user = update_entries(user)
    return user

def update_user(user):
    #TODO have to make some corrupted data to test this...
    user.version = version
    try:
        user.user_name    
    except AttributeError:
        #no version on user meaning made before versions implemented
        print("User name corrupted, changing to Default + TimeStamp")
        user.user_name = "Default" + get_timestamp

    try:
        user.weight
        if(user.weight == 0): raise AttributeError
    except AttributeError:
        print("Weight value corrupted, setting to 1.0")
        user.weight = 1.0
    
    try:
        user.goal_weight
        if(user.weight == 0): raise AttributeError
    except AttributeError:
        print("Goal weight corrupted, setting to 1.0")
        user.goal_weight = 1.0
    
    try:
        user.feet
    except AttributeError:
        print("User feet corrupted, setting to 1")
        user.feet = 1
    
    try:
        user.inches
    except AttributeError:
        print("User inches corrupted, setting to 1")
        user.feet = 1

    try:
        user.calorie_goal
    except AttributeError:
        print("User calorie goal corrupted, setting to 1")
        user.calorie_goal = 1
    
    try:
        user.start_date
    except AttributeError:
        print("User start date corrupted, setting to now.")
        user.start_date = datetime.date.today()
    
    try:
        user.motd
    except AttributeError:
        print("MOTD corrupted, setting to \"Do your best!\"")
        user.motd = "Do your best!"
    return user

#check entry attributes to work with current version.
def update_entries(user):
    #update to 1.0
    for d in user.entries.keys():
        print(user.entries[d])
        try:
            user.entries[d].goal_weight
            if user.entries[d].goal_weight == 0: raise AttributeError
        except AttributeError:
            print("Following Entry has no goal weight, using goal weight user currently has.")
            print("    ", str(user.entries[d]))
            user.entries[d].goal_weight = user.goal_weight
        
        try:
            user.entries[d].weight
            if user.entries[d].weight == 0: raise AttributeError
        except AttributeError:
            print("\nFollowing Entry has no weight, using weight user currently has.")
            print("    ", str(user.entries[d]))
            print("\n")
            user.entries[d].weight = user.weight
    return user

def check_for_entry(date_to_load):
    if not (loaded_date in user.entries):
        user.entries[loaded_date] = Entry(loaded_date,user.calorie_goal)
        user.entries[loaded_date].weight = user.weight
        user.entries[loaded_date].goal_weight = user.goal_weight

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
            if sanity_check():
                journal = ""
                print("Entry cleared.")
        
        if(choice == "4"):
            return journal

def is_pos_float(var):
    try:
        v = float(var)
        if v <= 0 : raise ValueError
        return True
    except ValueError:
        return False
    print("Something terrible happened in is_pos_float")
    return False


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

def is_pos_int(var):
    try:
        v = int(var)
        if v <= 0 : raise ValueError
        return True
    except ValueError:
        return False
    print("Something terrible happened in is_pos_int")
    return False


def get_bmi(feet,inches,weight):
    metric_weight = float(weight) * 0.453592
    total_height = int(feet) + float((float(inches)/12))
    metric_height = total_height * 0.3048

    bmi = metric_weight /(metric_height**2)

    return bmi


def settings_menu(user):
    while(True):
        print("\n\n\n")
        print("1. Change Goals")
        print("2. Change height")
        print("3. Edit MOTD")
        print("4. Change/Create Profile")
        print("5. Back")
        print("\n")
        choice = input("Your choice: ")
        if(choice == "1"):
            if(loaded_date == datetime.date.today()):
                user.goal_weight = get_pos_float_from_user("What is your goal weight?: ")
                user.calorie_goal = get_pos_int_from_user("What is your daily calorie goal?: ")
                user.entries[loaded_date].goal_weight = user.goal_weight
                user.entries[loaded_date].calorie_goal = user.calorie_goal
            else:
                print("Do you want to change the goals for this date in the past?")
                if(sanity_check):
                    user.entries[loaded_date].goal_weight = get_pos_float_from_user("What is your goal weight?: ")
                    user.entries[loaded_date].calorie_goal = get_pos_int_from_user("What is your daily calorie goal?: ")
        elif(choice == "2"):
            print("\n")
            user.feet = get_pos_int_from_user("How many feet tall are you?: ")
            user.inches = get_pos_int_from_user("How many inches tall are you?: ")
        elif(choice == "3"):
            print("\n")
            user.motd = input("Enter new MOTD: ")
        elif(choice == "4"):
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
        elif(choice == "5"):
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
                if sanity_check(): 
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

def sanity_check():
    check = input("Are you sure? y/n: ")
    if(check == "y"):
        return True
    else:
        return False

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

#Handle command line arguments.
if len(sys.argv) == 2:
    #print("One argument passed.")

    if sys.argv[1] =='-cc':
        print (user.entries[loaded_date].total_calories())
    
    if sys.argv[1] == '-cl':
        print (int(user.entries[loaded_date].calorie_goal) - user.entries[loaded_date].total_calories())
 
    if sys.argv[1] == '-cg':
        print (user.entries[loaded_date].calorie_goal)

    quit()


#user wants to add food.
if len(sys.argv) == 3:

    if not is_pos_int(sys.argv[2]):
        print("Adding Food: cc.py <foodname> <calories>.  Calories must be a whole positive number.")
        quit()

    user.entries[loaded_date].food.append(Food(sys.argv[1],sys.argv[2]))
    save_user(user)
    quit();    
    

elif len(sys.argv) > 3:
    print("I don't recognize those arguments. Please seek help.")
    quit()

while(True):
    save_user(user) #auto-save ;)
    check_for_entry(loaded_date)
    print("\n")
    print("\n")
    print("\n")
    print(f"Welcome {user.user_name}!")
    print("Entry for: ")
    print ("< ",loaded_date.strftime("%A the %d of %B, %Y")," >")
    print ("Calorie goal: ", user.entries[loaded_date].calorie_goal)
    print ("Calories left: ", int(user.entries[loaded_date].calorie_goal) - user.entries[loaded_date].total_calories() )
    bmi = get_bmi(user.feet,user.inches,user.entries[loaded_date].weight)
    bmidesc = ""
    if(bmi < 18.5):
        bmidesc = "underweight"
    elif(bmi <= 24.9):
        bmidesc = "healthy"
    elif(bmi <= 29.9):
        bmidesc = "overweight"
    elif(bmi > 29.9):
        bmidesc = "obese"
    print ("Goal weight: %.1f" % (float(user.entries[loaded_date].goal_weight)))
    print ("Your weight: %.1f BMI: %.1f (%s)" % (float(user.entries[loaded_date].weight), bmi, bmidesc))
    print ("You are ", int(user.entries[loaded_date].weight) - int(user.entries[loaded_date].goal_weight) , " pounds from your goal weight!")
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
        if(loaded_date == datetime.date.today()):
            print("Brave enough to get on a scale huh?")
            user.weight = get_pos_float_from_user("What is your weight now: ")
            user.entries[loaded_date].weight = user.weight
        else:
            print("Do you want to change the weight that you were on this date?")
            if(sanity_check):
                user.entries[loaded_date].weight = get_pos_float_from_user("What was your weight? ")
        
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
        calories = input("How many calories? (x to cancel) ")
        if calories is not "x" and is_pos_int(calories):
            user.entries[loaded_date].food.append(Food(choice, calories))
            print("Food added to your list!")
        else:
            print("Please try again, make sure you use a positive whole number of calories.")
    



