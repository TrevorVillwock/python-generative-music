from music import Music
from ambient_sounds import AmbientSounds
from pyo import Server, Mixer
import sys
import time

s = Server().boot()
s.start()

class Main():  
    def __init__(self):
        self.input_is_valid = 0
        self.music = Music("ionian") # default mode
        self.ambient_sounds = AmbientSounds()
        self.mixer = Mixer(outs=2, chnls=2, mul=0).out()
        print("\n\nWelcome to CASTLE OF SOUND\n\n")
        self.action_selection = input("What do you want to do?\n\n 1 - Eat food (Ionian)\n 2 - Go to the river (Dorian)\n 3 - Go to the top of the castle (Phrygian)\n 4 - Go to the garden (Lydian)\n 5 - Go for a hike (Mixolydian) \n 6 - Swim in the river (Aeolian) \n 7 - Go to the dungeon (Locrian)\n q - Quit \n\n Input a number or letter to choose: ")
        while self.input_is_valid == 0:
            match self.action_selection:
                case "1": 
                    # don't need to change modes since the default is ionian
                    self.ambient_sounds.start_first_sound("dining_hall")
                    self.input_is_valid = 1
                case "2": 
                    self.music.change_mode("dorian")
                    self.ambient_sounds.start_first_sound("river")
                    self.input_is_valid = 1
                case "3": 
                    self.music.change_mode("phrygian")
                    self.ambient_sounds.start_first_sound("wind")
                    self.input_is_valid = 1
                case "4": 
                    self.music.change_mode("lydian")
                    self.ambient_sounds.start_first_sound("birds")
                    self.input_is_valid = 1
                case "5": 
                    self.music.change_mode("mixolydian")
                    self.ambient_sounds.start_first_sound("footsteps")
                    self.input_is_valid = 1
                case "6": 
                    self.music.change_mode("aeolian")
                    self.ambient_sounds.start_first_sound("underwater")
                    self.input_is_valid = 1
                case "7": 
                    self.music.change_mode("locrian")
                    self.ambient_sounds.start_first_sound("dungeon")
                    self.input_is_valid = 1
                case "q":
                    # fade master volume
                    # TODO: fix clicking noise when stopping
                    self.mixer.setMul(0.0)
                    self.music.stop()
                    time.sleep(1)
                    s.stop()
                    sys.exit()
                case _:
                    self.action_selection = input("Please enter a number between 1 and 7:")

        self.mixer.addInput(3, self.ambient_sounds.sound1)
        self.mixer.addInput(4, self.ambient_sounds.sound2)
        self.mixer.setAmp(0, 0, 0.1)
        self.mixer.setAmp(1, 0, 0.1)
        self.mixer.setAmp(2, 0, 0.1)
        self.mixer.setAmp(3, 0, 0.5)
        self.mixer.setTime(0.01)
        self.mixer.setMul(1)
        self.run_input_loop()
        
    def run_input_loop(self):
        user_command = None
        while user_command != "q":
            user_command = input("\n\nEnter next command: ")
            match user_command:
                case "1": 
                    self.music.change_mode("ionian")
                    self.ambient_sounds.change_sound("dining_hall")
                case "2": 
                    self.music.change_mode("dorian")
                    self.ambient_sounds.change_sound("river")
                case "3": 
                    self.music.change_mode("phrygian")
                    self.ambient_sounds.change_sound("wind")
                case "4": 
                    self.music.change_mode("lydian")
                    self.ambient_sounds.change_sound("birds")
                case "5": 
                    self.music.change_mode("mixolydian")
                    self.ambient_sounds.change_sound("footsteps")
                case "6": 
                    self.music.change_mode("aeolian")
                    self.ambient_sounds.change_sound("underwater")
                case "7": 
                    self.music.change_mode("locrian")
                    self.ambient_sounds.change_sound("dungeon")
                case "q":
                    # fade master volume
                    # TODO: fix clicking noise when stopping
                    self.mixer.setMul(0.0)
                    self.music.stop()
                    time.sleep(2)
                    s.stop()
                    sys.exit()
                case _:
                    self.action_selection = input("Please enter a valid command: ")
            # print(user_command)
            
main = Main()

s.gui(locals)