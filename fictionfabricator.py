import sys # to help run multiple programs within terminal
import random # for random calculations
import threading # for playing multiple sounds at once


from textx import metamodel_from_file # metamodel imported to textx
from playsound import playsound # for audio

tale_file = sys.argv[1] # obtain file based on the argument taken from the terminal
fiction_mm = metamodel_from_file('fictionfabricator.tx') # generate grammar meta_model
fiction_model = fiction_mm.model_from_file(tale_file) # generate a model based on the program created from terminal

# colors for text
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
BLACK = '\033[30m'
RESET = '\033[0m'

state = {} # keeps track of state for variables 

# variable map keeps track of any 'items' or 'personalities' created within the program (story)
def variablemap(variable, state):
    selected_value = state[variable]
    return selected_value

# evaluate variable checks if a variable is properly defined, if so, put it into the dictionary 
def evaulate_variable(variable, state):
    if variable in state:
        return variablemap(variable, state)
    else:
        raise Exception(f"Variable '{variable}' is not defined")

def check_bool(item):
    if item == "true":
        return True
    else:
        return False

class Character:
    def __init__(self, name, personalities_list=None):
        self.name = name
        self.personalities_list = personalities_list or []

class FictionFabricator:
    def interpret(self, model):
        # parses every statement (declaration) within a program (story) 
        for index, c in enumerate(model.declarations):
            # if the statment is a CreateCharacter statement
            if c.__class__.__name__ == "CreateCharacter":
                name = c.title
                main_character = Character(name)
                print(f"Your character's name is {YELLOW}{main_character.name}{RESET}.")
                print(f"{GREEN}Their Characteristics:{RESET}")
                for index, personality in enumerate(c.personalities):
                    state[personality.characteristic] = personality.value
                    if not index+1 == len(c.personalities):
                        print(f"{RED}{personality.characteristic}{RESET} with {YELLOW}{personality.value}{RESET} value points.")
                    else:
                         print(f"{RED}{personality.characteristic}{RESET} with {YELLOW}{personality.value}{RESET} value points.")
                for index, item in enumerate(c.items):
                    item.value = check_bool(item.value)
                    state[item.gear] = item.value
                    if item.value:
                        print(f"{YELLOW}{name}{RESET} holds a(n) {GREEN}{item.gear}{RESET}.")
                    else:
                        print(f"{YELLOW}{name}{RESET} does not hold a(n) {GREEN}{item.gear}{RESET}.")
            # if the statment is an EditCharacter statement
            elif c.__class__.__name__ == "EditCharacter":
                if (name == main_character.name):
                    user_input = input("Please enter the character's new name!\n")
                    name = user_input
                    print(f"{GREEN}{c.title}{RESET} is now called {YELLOW}{name}{RESET}.")
            # if the statment is an Setting statement
            elif c.__class__.__name__ == "Setting":
                # there are three templates for setting: boat, mansion, and forest: each print a basic template for the user
                if (c.setting == "boat"): # if user types boat
                    print(f"{name}'s awoken inside a dimly-lit ramshackle room. They're surrounded by its wooden exterior and hear its bellows " 
                    "and groans recurrently. With the muted splashing of waves from outside, they acknowledge that they are atop a vessel setting out "
                    f"voyage somewhere. From the bed {name} laid on, they see a soft yellow light leering through the window.")
                    playsound("SeaWaves.wav")
                elif (c.setting == "mansion"): # if user types mansion
                    print(f"{name} walks up to a mysterious mansion. It towers above them, with its windows glaring downward towards"
                          f" towards their minute stature. As they push open the mansions' doors, dust and cobwebs fly into the air. Within the mansion"
                          f" shows that there are no windows and no doors, what's {name} to do?")
                    playsound("shipCreak.wav")
                elif (c.setting == "forest"): # if user types forest
                    print(f"{name} is currently running away from a group of headless phantoms. Their maniacal cackling and long, sharp finger bones disuade anyone form "
                          f"ever getting close, but our hero didn't listen to the warnings. As {name} enters deeper into the forest, the pleasant sunlight "
                          f"quickly fades into darkness and shrubery. They lost the phantoms, but where are they to go?")  
                    playsound("LeavesRustle.wav")
                    # for loop that iterates through each decision 
                    for index, choice in enumerate(c.decisions):
                        variable = choice.variable[index] # gets name of variable in if statement
                        requirement = choice.requirement[index] # gets name of requirement in if statement
                        if not variable == None:
                            try:
                                print(f"{RED}HEADS UP: {RESET}Option {index+1} requires a(n) {GREEN}{variable}{RESET} score greater than {YELLOW}{requirement}{RESET}.")
                                print(f"{BLUE}Option {index+1}:{RESET} {choice.first_choice}") # prints first choice option
                            except IndexError: # if there is no option available
                                print(f"Nothing.")
                            try:
                                print(f"{RED}HEADS UP: {RESET}Option {index+2} requires a(n) {GREEN}{variable}{RESET} score less than {YELLOW}{requirement}{RESET}.")
                                print(f"{CYAN}Option {index+2}:{RESET} {choice.second_choice}") # prints second choice option
                            except IndexError: # if there is no option available
                                print(f"Nothing.")
                            user_input = input(f"Choose the path you'd like {YELLOW}{name}{RESET} to take > ") # ask user for input
                            # for loop that iterates through each decision, again, with a different name?
                            for index, path in enumerate(c.decisions):
                                if (user_input == '1'): 
                                        index_of_variable = path.variable[index]  # gets name of variable in if statement from a list
                                        index_of_requirement = path.requirement[index]  # gets name of requirement in if statement from a list
                                        if '>' in path.check: # if an if statement has > symbol within it
                                            if state[(index_of_variable)] > index_of_requirement: # if the user's variable value is greater than the value declared by the if statement...
                                                print(path.responses[0].response) 
                                                try:
                                                    print(f"{YELLOW}{name}:{RESET} {GREEN}{path.dialogue[0].dialogue}{RESET}") # grabs dialogue from within a list of a list
                                                except IndexError: # no dialogue given
                                                    print(f"{YELLOW}{name}:{RESET} {GREEN}'...'{RESET}")
                                            else:
                                                print(f"{GREEN}You are much too beauitful to move forward with this action!{RESET}") # if not less than, print this
                                elif (user_input == '2'):
                                    print(path.responses[1].response)
                                    try:
                                        print(f"{YELLOW}{name}:{RESET} {GREEN}{path.dialogue[1].dialogue}{RESET}") # grabs dialogue from within a list of a list
                                    except IndexError: # no dialogue given
                                        print(f"{YELLOW}{name}:{RESET} {GREEN}'...'{RESET}") 

                else:
                    # custom setting option
                    print(c.setting)
                    playsound("CustomSound.mp3")
                    # for loop that iterates through every possible decision
                    for index, choice in enumerate(c.decisions):
                        # provies both choices
                        print(f"{BLUE}Option {index+1}:{RESET} {choice.first_choice}")
                        print(f"{CYAN}Option {index+2}:{RESET} {choice.second_choice}")
                        user_input = input(f"Choose the path you'd like {YELLOW}{name}{RESET} to take > ")
                        for index, path in enumerate(c.decisions): # within the decisions, determine which user choses
                            if (user_input == '1'):
                                    print(path.responses[0].response)
                                    try:
                                        print(f"{YELLOW}{name}:{RESET} {GREEN}{path.dialogue[0].dialogue}{RESET}") # grabs dialogue from within a list of a list
                                    except IndexError: # no dialogue given
                                        print(f"{YELLOW}{name}:{RESET} {GREEN}'...'{RESET}")
                            elif (user_input == '2'):
                                    print(path.responses[1].response)
                                    try:
                                        print(f"{YELLOW}{name}:{RESET} {GREEN}{path.dialogue[1].dialogue}{RESET}") # grabs dialogue from within a list of a list
                                    except IndexError: # no dialogue given
                                        print(f"{YELLOW}{name}:{RESET} {GREEN}'...'{RESET}")
            # if the statment is an Dialogue statement
            elif c.__class__.__name__ == "Dialogue":
                print(f"{YELLOW}{name}:{RESET} {GREEN}'{c.dialogue}' {RESET}")
            # if the statment is an DiceRoll statement
            elif c.__class__.__name__ == "DiceRoll":
                diceSize = c.amount
                diceRoll = random.randint(1, diceSize) # choses size of die and rolls it
                print(f"{YELLOW}{name}{RESET} has rolled a {GREEN}{diceRoll}{RESET}.")
            # if the statment is an Continue statement
            elif c.__class__.__name__ == "Continue":
                # loop statement that iterates on specific declarations based on a number chosen
                for i in range(c.times):
                    for declaration in c.declarations: # for loop that parses every declaration available
                        # can loop "Dialogue" and "DiceRoll" statements as many times a user wants
                        if declaration.__class__.__name__ == "Dialogue":
                            print(f"{YELLOW}{name}:{RESET} {GREEN}'{declaration.dialogue}' {RESET}")
                        elif declaration.__class__.__name__ == "DiceRoll":
                            diceSize = declaration.amount
                            diceRoll = random.randint(1, diceSize)
                            print(f"{YELLOW}{name}{RESET} has rolled a {GREEN}{diceRoll}{RESET}.")                        
                      
BasicTale = FictionFabricator() # creates a basicTale python object
BasicTale.interpret(fiction_model) #basicTale interprets the program(story) we give it