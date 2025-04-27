import sys
import random
from textx import metamodel_from_file
from playsound import playsound

tale_file = sys.argv[1]
fiction_mm = metamodel_from_file('fictionfabricator.tx')
fiction_model = fiction_mm.model_from_file(tale_file)

#Colors for Text
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
BLACK = '\033[30m'
RESET = '\033[0m'

state = {}

def variablemap(variable, state):
    selected_value = state[variable]
    return selected_value

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
        for index, c in enumerate(model.declarations):
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

            elif c.__class__.__name__ == "EditCharacter":
                if (name == main_character.name):
                    user_input = input("Please enter the character's new name!\n")
                    name = user_input
                    print(f"{GREEN}{c.title}{RESET} is now called {YELLOW}{name}{RESET}.")
            elif c.__class__.__name__ == "Setting":
                if (c.setting == "boat"):
                    print(f"{name}'s awoken inside a dimly-lit ramshackle room. They're surrounded by its wooden exterior and hear its bellows " 
                    "and groans recurrently. With the muted splashing of waves from outside, they acknowledge that they are atop a vessel setting out "
                    f"voyage somewhere. From the bed {name} laid on, they see a soft yellow light leering through the window.")
                    playsound("SeaWaves.wav")
                elif (c.setting == "mansion"):
                    print(f"{name} walks up to a mysterious mansion. It towers above them, with its windows glaring downward towards"
                          f" towards their minute stature. As they push open the mansions' doors, dust and cobwebs fly into the air. Within the mansion"
                          f" shows that there are no windows and no doors, what's {name} to do?")
                    playsound("shipCreak.wav")
                elif (c.setting == "forest"):
                    print(f"{name} is currently running away from a group of headless phantoms. Their maniacal cackling and long, sharp finger bones disuade anyone form "
                          f"ever getting close, but our hero didn't listen to the warnings. As {name} enters deeper into the forest, the pleasant sunlight "
                          f"quickly fades into darkness and shrubery. They lost the phantoms, but where are they to go?")  
                    playsound("LeavesRustle.wav")
                    for index, choice in enumerate(c.decisions):
                        try:
                            print(f"{BLUE}Option {index+1}:{RESET} {choice.first_choice}")
                        except IndexError:
                            print(f"Nothing...")
                        try:
                            print(f"{CYAN}Option {index+2}:{RESET} {choice.second_choice}")
                        except IndexError:
                            print(f"Nothing.")
                        user_input = input(f"Choose the path you'd like {YELLOW}{name}{RESET} to take > ")
                        for index, path in enumerate(c.decisions):
                            if (user_input == '1'):
                                    print(path.responses[0].response)
                                    try:
                                        print(f"{YELLOW}{name}:{RESET} {GREEN}{path.dialogue[0].dialogue}{RESET}")
                                    except IndexError:
                                        print(f"{YELLOW}{name}:{RESET} {GREEN}'...'{RESET}")
                            elif (user_input == '2'):
                                    print(path.responses[1].response)
                                    try:
                                        print(f"{YELLOW}{name}:{RESET} {GREEN}{path.dialogue[1].dialogue}{RESET}")
                                    except IndexError:
                                        print(f"{YELLOW}{name}:{RESET} {GREEN}'...'{RESET}")         
                else:
                    print(c.setting)
                    playsound("CustomSound.mp3")
                    for index, choice in enumerate(c.decisions):
                        print(f"{BLUE}Option {index+1}:{RESET} {choice.first_choice}")
                        print(f"{CYAN}Option {index+2}:{RESET} {choice.second_choice}")
                        user_input = input(f"Choose the path you'd like {YELLOW}{name}{RESET} to take > ")
                        for index, path in enumerate(c.decisions):
                            if (user_input == '1'):
                                    print(path.responses[0].response)
                                    try:
                                        print(f"{YELLOW}{name}:{RESET} {GREEN}{path.dialogue[0].dialogue}{RESET}")
                                    except IndexError:
                                        print(f"{YELLOW}{name}:{RESET} {GREEN}'...'{RESET}")
                            elif (user_input == '2'):
                                    print(path.responses[1].response)
                                    try:
                                        print(f"{YELLOW}{name}:{RESET} {GREEN}{path.dialogue[1].dialogue}{RESET}")
                                    except IndexError:
                                        print(f"{YELLOW}{name}:{RESET} {GREEN}'...'{RESET}")
            elif c.__class__.__name__ == "Dialogue":
                print(f"{YELLOW}{name}:{RESET} {GREEN}'{c.dialogue}' {RESET}")
            elif c.__class__.__name__ == "DiceRoll":
                diceSize = c.amount
                diceRoll = random.randint(1, diceSize)
                print(f"{YELLOW}{name}{RESET} has rolled a {GREEN}{diceRoll}{RESET}.")
            elif c.__class__.__name__ == "Continue":
                for i in range(c.times):
                    for declaration in c.declarations:
                        if declaration.__class__.__name__ == "Dialogue":
                            print(f"{YELLOW}{name}:{RESET} {GREEN}'{declaration.dialogue}' {RESET}")
                        elif declaration.__class__.__name__ == "DiceRoll":
                            diceSize = declaration.amount
                            diceRoll = random.randint(1, diceSize)
                            print(f"{YELLOW}{name}{RESET} has rolled a {GREEN}{diceRoll}{RESET}.")
                        
                      
BasicTale = FictionFabricator()
BasicTale.interpret(fiction_model)