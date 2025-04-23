from textx import metamodel_from_file
from playsound import playsound

fiction_mm = metamodel_from_file('fictionfabricator.tx')
fiction_model = fiction_mm.model_from_file('program1.tale')


class Character:
    def __init__(self, name, personalities_list=None):
        self.name = name
        self.personalities_list = personalities_list

    def __str__(self):
        return f"Your character's name is {self.name}."


class FictionFabricator:
    def interpret(self, model):
        for index, c in enumerate(model.declarations):
            if c.__class__.__name__ == "CreateCharacter":
                name = c.title
                main_character = Character(name)
                print(f"Your character's name is {main_character.name}.")
                print("Their Characteristics:")
                for index, personality in enumerate(c.personalities):
                    if not index+1 == len(c.personalities):
                        print(f"{personality.characteristic} with {personality.value} value points.")
                    else:
                         print(f"{personality.characteristic} with {personality.value} value points.")
            elif c.__class__.__name__ == "EditCharacter":
                if (name == main_character.name):
                    user_input = input("Please enter the character's new name!\n")
                    name = user_input
                    print(f"{c.title} is now called {name}.")
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
                    print(f"{name} is currently running away from a group of headless phantoms. Their maniacal cackling and long, sharp finger bones disuade anyone form"
                          f"ever getting close, but our hero didn't listen to the warnings. As {name} enters deeper into the forest, the pleasant sunlight"
                          f"quickly fades into darkness and shrubery. They lost the phantoms, but where are they to go?")   

                    playsound("LeavesRustle.wav")           
                else:
                    print(c.setting)
                    playsound("CustomSound.mp3")
                    for index, choice in enumerate(c.decisions):
                        print(f"Option {index+1}: {choice.first_choice}")
                        print(f"Option {index+2}: {choice.second_choice}")
                        user_input = input(f"Choose the path you'd like {name} to take > ")
                        for index, path in enumerate(c.decisions):
                            if (user_input == '1'):
                                    print(path.responses[0].response)
                                    print(f"{name}: {path.dialogue.dialogue}")
                            elif (user_input == '2'):
                                    print(path.responses[1].response)
            elif c.__class__.__name__ == "Check":
                if name == main_character.name:
                    print(main_character)
                    print(f"Your character's personalities are:")
            elif c.__class__.__name__ == "Dialogue":
                print(f'{name}: "{c.dialogue}" ')
        
BasicTale = FictionFabricator()
BasicTale.interpret(fiction_model)