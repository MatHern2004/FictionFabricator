import sys # helps run multiple programs within terminal
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
GREY = '\033[30m'
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


# checks if an item is marked as true or false 
def check_bool(item_result, item_name):
    if not item_name == '': # if an item exists...
        true_value = state[item_name]
        if true_value == item_result[0]:
            return True
        else:
            return False
    else:
        return False # if it doesn't exist return false


class Character:
    def __init__(self, name, personalities_list=None):
        self.name = name
        self.personalities_list = personalities_list


def make_decision(decision_data, character):
    for index, choice in enumerate(decision_data): # iterates through the possible declarations one can make within a decision statement
   
    # obtain all needed variables at inception
        first_choice = choice.first_choice
        second_choice = choice.second_choice
        variable_one = choice.variable_one 
        requirement_one = choice.requirement_one
        variable_two = choice.variable_two
        requirement_two = choice.requirement_two
        response_one = choice.responses[index].response if choice.responses[index].response else ""# grabs first option from a list of responses
        response_two = choice.responses[index].response if choice.responses[index].response else ""# grabs second option from a list of responses
        item_one = choice.item_one
        item_two = choice.item_two
        item_one_result = choice.result
        item_two_result=choice.result
        check_one = choice.check_one
        check_two = choice.check_two
        empty_one = choice.empty_one
        empty_two = choice.empty_two
        dialogue_one = choice.dialogue_one.dialogue if choice.dialogue_one else "" # if dialogue isn't provided, it creates a blank value
        dialogue_two = choice.dialogue_two.dialogue if choice.dialogue_two else "" # if dialogue isn't provided, it creates a blank value

     # display option 1
        if not check_one == None: # if there is a check
            print(f"{RED}HEADS UP: {RESET}Option 1 requires that {GREEN}{variable_one}{RESET} {check_one} {YELLOW}{requirement_one}{RESET}.")
            print(f"{BLUE}Option 1:{RESET} {first_choice}\n") 
        else:
            if not item_one == '': # if there is an item
                print(f"{RED}HEADS UP: {RESET}Option 1 requires that {GREEN}{item_one}{RESET} = {YELLOW}{item_one_result}{RESET}.")
                print(f"{BLUE}Option 1:{RESET} {first_choice}\n") 
            elif "" == first_choice: # if there is no choice given
                print(f"{BLUE}Option 1{RESET} is unavailable...")
            else:
                print(first_choice) # if there is no requirement ('item' or 'key')
                print(f"{BLUE}Option 1:{RESET} {first_choice}\n") 
  
    # display option 2
        if not check_two == None: # if there is a check
            print(f"{RED}HEADS UP: {RESET}Option 2 requires that {GREEN}{variable_two}{RESET} {check_two} {YELLOW}{requirement_two}{RESET}.")
            print(f"{BLUE}Option 2:{RESET} {second_choice}\n") 
        else:
            if not item_two == '': # if there is an item
                print(f"{RED}HEADS UP: {RESET}Option 2 requires that {GREEN}{item_two}{RESET} = {YELLOW}{item_two_result}{RESET}.")
                print(f"{BLUE}Option 2:{RESET} {second_choice}\n") 
            elif "" == second_choice: # if there is no choice given
                print(f"{BLUE}Option 2{RESET} is unavailable...")
            else:
                print(second_choice) # if there is no requirement ('item' or 'key')
                print(f"{BLUE}Option 2:{RESET} {second_choice}\n") 
    
    user_input = input(f"Choose the path you'd like {YELLOW}{character.name}{RESET} to take > ")


# Begin selection process
    if (user_input == "1"): # if user selects 1
        inequality_flag = check_inequality(check_one, variable_one, requirement_one)
        if inequality_flag:
            print(f"{GREEN}Option 1:{RESET} {response_one}\n")
            say_dialogue(dialogue_one, character)
            if not choice.new_setting_one == None: # if there is a goto
                print(f"{YELLOW}We'll be heading to a new location!{RESET}")
                locals = choice.new_setting_one.locations[0].location # statement that tells us where we're going
                print(f"{locals}\n")
                return locals # statement for later use in our goto-function
        elif inequality_flag == None or inequality_flag == False: 
            if check_bool(item_one_result, item_one): # if statement that checks for a item boolean
                print(f'{YELLOW}{character.name}{RESET} uses their {GREEN}{item_one}{RESET} well and with ease.')
                print(f"{GREEN}Option 1:{RESET} {response_one}\n")
                say_dialogue(dialogue_one, character)
                if not choice.new_setting_one == None: # if there is a goto statement within...
                    print(f"{YELLOW}We'll be heading to a new location!{RESET}")
                    locals = choice.new_setting_one.locations[0].location # statement that tells us where we're going
                    print(f"{locals}\n")
                    return locals # statement for later use in our goto-function
            elif empty_one == "yes": # if the choice has no requirements
                print(f"{GREEN}Option 1:{RESET} {response_one}")
                say_dialogue(dialogue_one, character)
            else: # go to option 2
                print(f"{RED}You do not meet the requirements to make this choice!{RESET}\n")
                print("You will be taken to Option 2.")
                inequality_flag = check_inequality(check_two, variable_two, requirement_two)
                if inequality_flag: 
                    print(f"{GREEN}You meet the requirements for the second option!{RESET}\n")
                    print(f"{GREEN}Option 2:{RESET} {response_two}")
                    say_dialogue(dialogue_two, character)
                    if not choice.new_setting_two == None: # if there is a goto
                        print(f"{YELLOW}We'll be heading to a new location!{RESET}")
                        locals = choice.new_setting_two.locations[0].location # statement that tells us where we're going
                        print(f"{locals}\n")
                        return locals # statement for later use in our goto-function
                elif inequality_flag == None or inequality_flag == False:
                    if check_bool(item_two_result, item_two): # if statement that checks for a item boolean
                        print(f'{YELLOW}{character.name}{RESET} uses their {GREEN}{item_two}{RESET} well and with ease.')
                        print(f"{GREEN}Option 2:{RESET} {response_two}")
                        say_dialogue(dialogue_two, character)
                        if not choice.new_setting_two == None: # if there is a goto statement within...
                            print(f"{YELLOW}We'll be heading to a new location!{RESET}")
                            locals = choice.new_setting_two.locations[0].location # statement that tells us where we're going
                            print(f"{locals}\n")
                            return locals # statement for later use in our goto-function
                    elif empty_two == "yes": # if the choice has no requirements
                        print(f"{GREEN}Option 2:{RESET} {response_two}")
                        say_dialogue(dialogue_two, character) 
                    else: # if neither of the options meet the requirements
                        print(f"{RED}You do not meet the requirements to make this choice!{RESET}")
                        print(f"{RED}Neither{RESET} of the variants are accessible...\n")
                        print(f"{YELLOW}YOU LOSE!{RESET}")
        

    else: # if user selects 2
        inequality_flag = check_inequality(check_two, variable_two, requirement_two)
        if inequality_flag:
            print(f"{GREEN}Option 2:{RESET} {response_two}\n")
            say_dialogue(dialogue_two, character)
            if not choice.new_setting_two == None:
                print(f"{YELLOW}We'll be heading to a new location!{RESET}")
                locals = choice.new_setting_two.locations[0].location # statement that tells us where we're going
                print(f"{locals}\n")
                return locals # statement for later use in our goto-function
        elif inequality_flag == None or inequality_flag == False:
            if check_bool(item_two_result, item_two): # if statement that checks for a item boolean
                print(f'{YELLOW}{character.name}{RESET} uses their {GREEN}{item_two}{RESET} well and with ease.')
                print(f"{GREEN}Option 2:{RESET} {response_two}\n")
                say_dialogue(dialogue_two, character)
                if not choice.new_setting_two == None: # if there is a goto statement within...
                    print(f"{YELLOW}We'll be heading to a new location!{RESET}")
                    locals = choice.new_setting_two.locations[0].location # statement that tells us where we're going
                    print(f"{locals}\n")
                    return locals # statement for later use in our goto-function
            elif empty_two == "yes": # if the choice has no requirements
                print(f"{GREEN}Option 2:{RESET} {response_two}")
                say_dialogue(dialogue_two, character)
            else: # go to option 1
                print(f"{RED}You do not meet the requirements to make this choice!{RESET}\n")
                print("You will be taken to Option 1.")
                inequality_flag = check_inequality(check_one, variable_one, requirement_one)
                if inequality_flag:
                    print(f"{GREEN}You meet the requirements for the second option!{RESET}\n")
                    print(f"{GREEN}Option 1:{RESET} {response_one}")
                    say_dialogue(dialogue_one, character)
                    if not choice.new_setting_one == None:
                        print(f"{YELLOW}We'll be heading to a new location!{RESET}")
                        locals = choice.new_setting_one.locations[0].location # statement that tells us where we're going
                        print(locals)
                        return locals # statement for later use in our goto-function
                elif inequality_flag == None or inequality_flag == False:
                    if check_bool(item_one_result, item_one): # if statement that checks for a item boolean
                        print(f'{YELLOW}{character.name}{RESET} uses their {GREEN}{item_one}{RESET} well and with ease.')
                        print(f"{GREEN}Option 1:{RESET} {response_one}")
                        say_dialogue(dialogue_one, character)
                        if not choice.new_setting_one == None: # if there is a goto statement within...
                            print(f"{YELLOW}We'll be heading to a new location!{RESET}")
                            locals = choice.new_setting_one.locations[0].location # statement that tells us where we're going
                            print(f"{locals}\n")
                            return locals # statement for later use in our goto-function
                    elif empty_one == "yes": # if the choice has no requirements
                            print(f"{GREEN}Option 1:{RESET} {response_one}")
                            say_dialogue(dialogue_one, character)
                    else: # if neither of the options meet the requirements
                        print(f"{RED}You do not meet the requirements to make this choice!{RESET}")
                        print(f"{RED}Neither{RESET} of the variants are accessible...\n")
                        print(f"{YELLOW}YOU LOSE!{RESET}")


def make_setting(setting_data, character):
     # there are three templates for setting: boat, mansion, and forest: each print a basic template for the user and play a noise
    if setting_data == "boat":
       print(f"{YELLOW}{character.name}'s{RESET} awoken inside a dimly-lit ramshackle room. They're surrounded by its wooden exterior and hear its bellows " 
       f"and groans recurrently. With the muted {BLUE}splashing of waves{RESET} from outside, they acknowledge that they are atop a vessel setting out "
       f"voyage somewhere. From the bed {YELLOW}{character.name}{RESET} laid on, they see a soft {YELLOW}yellow light{RESET} leering through the window.")
       playsound("SeaWaves.wav")
    elif setting_data == "mansion":
        print(f"{YELLOW}{character.name}{RESET} walks up to a mysterious mansion. It towers above them, with its windows {RED}glaring{RESET} downward towards"
        f" towards their minute stature. As they push open the mansions' doors, {RED}dust and cobwebs{RESET} fly into the air. Within the mansion"
        f" shows that there are no windows and no doors, what's {YELLOW}{character.name}{RESET} to do?")
        playsound("shipCreak.wav")
    elif setting_data == "forest":
        print(f"{YELLOW}{character.name}{RESET} is currently running away from a group of {RED}headless phantoms{RESET}. Their {YELLOW}maniacal cackling{RESET} and long, sharp finger bones disuade anyone form "
        f"ever getting close, but our hero didn't listen to the warnings. As {YELLOW}{character.name}{RESET} enters deeper into the {GREEN}forest{RESET}, the pleasant sunlight "
        f"quickly fades into darkness and shrubery. They lost the phantoms, but where are they to go?")  
        playsound("LeavesRustle.wav")
    else: # if neither of the options are chosen, allow for user defined setting
        print(f"{YELLOW}{character.name}:{RESET} {setting_data}")
        playsound("CustomSound.mp3")


def roll_dice(dice_data, character):
    dice_size = dice_data
    dice_roll = random.randint(1, dice_size)
    print(f"{YELLOW}{character.name}:{RESET} has rolled a {GREEN}{dice_roll}{RESET}")


def say_dialogue(statement_data, character):
    if not statement_data == '':
        print(f"{YELLOW}{character.name}:{RESET} {GREEN}{statement_data}{RESET}")


def loop(continue_data, character):
     for i in range(continue_data.times): # creates a loop that allows for multiple dialogue and diceroll statements. 
        for declaration in continue_data.declarations:
            if declaration.__class__.__name__ == "Dialogue":
                say_dialogue(declaration.dialogue, character)
            elif declaration.__class__.__name__ == "DiceRoll":
                roll_dice(declaration.amount, character)


    # edit name of character
def edit_character(character_data, character):
    user_input = input("Please enter the character's new name!\n")
    character = user_input
    print(f"{GREEN}{character_data}{RESET} is now called {YELLOW}{character}{RESET}.")
    return character
    

    # create character with name, personalities, and gear
def create_character(name_data, personality_data, item_data):
    character = Character(name_data)
    name = character.name
    print(f"Your character's name is {YELLOW}{name}{RESET}.")
    print(f"{GREEN}Their Characteristics:{RESET}")
    for index, personality in enumerate(personality_data): # iterate through list of personalities and place them into variablemap
        state[personality.characteristic] = personality.value
        print(f"{RED}{personality.characteristic}{RESET} with {YELLOW}{personality.value}{RESET} value points.")
    for index, item in enumerate(item_data):  # iterate through list of items and place them into variablemap
        state[item.gear] = item.value
        if item.value == 'true': # if the player has an item
            print(f"{YELLOW}{name}{RESET} holds a(n) {GREEN}{item.gear}{RESET}.")
        else:
            print(f"{YELLOW}{name}{RESET} does not hold a(n) {GREEN}{item.gear}{RESET}.")
        return character


    # if 'goto' statement made, user will go to a new setting
def make_goto(goto_data, goto_location, character):
    for index, place in enumerate(goto_data): # iterates through goto statements 
        locals = place.location[index]
        if locals == None or goto_location == None: # if there is no goto location provided
            print(f"You passed by a path you could've taken, {RED}but you made your choice.{RESET}")
        elif locals in goto_location:
            make_decision(place.decisions, character) # if there is then reveal its choices


def check_inequality(choice_data, variable, requirement):
    if choice_data == None: # if there is no choice data
        return None
    
    if '<=' in choice_data:
        result = state[variable] <= requirement
        return result
    elif '>=' in choice_data:
        result = state[variable] >= requirement
        return result
    elif '==' in choice_data:
        result = state[variable] == requirement
        return result
    elif '!=' in choice_data:
        result = state[variable] != requirement
        return result
    elif '<' in choice_data:
        result = state[variable] < requirement
        return result
    elif '>' in choice_data:
        result = state[variable] > requirement
        return result
    else:
        raise Exception(f"{RED}The inequality you entered is not valid, {choice_data}!{RESET}")


    # interprets any fictionfabricator program
class FictionFabricator:
    def interpret(self, model):
        # parses every statement (declaration) within a program (story) 
        for index, c in enumerate(model.declarations):
            # if the statment is a CreateCharacter statement
            if c.__class__.__name__ == "CreateCharacter":
                main_character = create_character(c.title, c.personalities, c.items)
            # if the statment is an EditCharacter statement
            elif c.__class__.__name__ == "EditCharacter":
                main_character.name = edit_character(c.title, main_character)
            # if the statment is an Setting statement
            elif c.__class__.__name__ == "Setting":
                make_setting(c.setting, main_character)
                # if a goto exists, then it will be set to a variable
                goto_location = make_decision(c.decisions, main_character)
            # if the statment is an Dialogue statement
            elif c.__class__.__name__ == "Dialogue":
                say_dialogue(c.dialogue, main_character)
            # if the statment is an DiceRoll statement
            elif c.__class__.__name__ == "DiceRoll":
                roll_dice(c.amount, main_character)
            # if the statment is an Continue statement
            elif c.__class__.__name__ == "Continue":
                loop(c, main_character)
            # if the statement is a Goto statement
            elif  c.__class__.__name__ == "Goto":
                make_goto(c.locations, goto_location, main_character)


BasicTale = FictionFabricator() # creates a basicTale python object
BasicTale.interpret(fiction_model) #basicTale interprets the program (story) we give it
# Error-handling.
# Make a website.