from music import Music
from ambient_sounds import AmbientSounds
from pyo import *

s = Server().boot()
s.start()

class Main():  
    def __init__(self):
        self.input_is_valid = 0
        self.mode = "Ionian" # default mode
        self.room_selection = input("Input a number to enter the corresponding room:\n\n 1. Ionian\n 2. Dorian\n 3. Phrygian\n 4. Lydian\n 5. Mixolydian\n 6. Aeolian\n 7. Locrian\n\n")
        while self.input_is_valid == 0:
            match self.room_selection:
                case "1": 
                    self.mode = "ionian"
                    self.input_is_valid = 1
                case "2": 
                    self.mode = "dorian"
                    self.input_is_valid = 1
                case "3": 
                    self.mode = "phrygian"
                    self.input_is_valid = 1
                case "4": 
                    self.mode = "lydian"
                    self.input_is_valid = 1
                case "5": 
                    self.mode = "mixolydian"
                    self.input_is_valid = 1
                case "6": 
                    self.mode = "aeolian"
                    self.input_is_valid = 1
                case "7": 
                    self.mode = "locrian"
                    self.input_is_valid = 1
                case _:
                    self.room_selection = input("Please enter a number between 1 and 7:")
        
        self.music = Music(self.mode)
        self.ambient_sounds = AmbientSounds()
        self.mixer = Mixer(chnls=2).out()
        
        # self.mixer.addInput(0, self.music.melody_reverb)
        # self.mixer.addInput(1, self.music.harmony_reverb)
        # self.mixer.addInput(2, self.music.bass_synth)
        self.mixer.addInput(3, self.ambient_sounds.sound1)
        self.mixer.addInput(4, self.ambient_sounds.sound2)
        self.mixer.setAmp(0, 0, 0.1)
        self.mixer.setAmp(1, 0, 0.1)
        self.mixer.setAmp(2, 0, 0.1)
        self.mixer.setAmp(3, 0, 0.5)
        self.run_input_loop()
        
    def run_input_loop(self):
        user_command = None
        while user_command != "q":
            user_command = input("Enter next command: ")
            match user_command:
                case "1": 
                    self.music.change_mode("ionian")
                    self.ambient_sounds.change_sound("dining_hall")
                case "2": 
                    self.music.change_mode("dorian")
                    self.ambient_sounds.change_sound("river")
                case "3": 
                    self.music.change_mode("phrygian")
                    self.ambient_sounds.change_sound("river")
                case "4": 
                    self.music.change_mode("lydian")
                    self.ambient_sounds.change_sound("birds")
                case "5": 
                    self.music.change_mode("mixolydian")
                    self.ambient_sounds.change_sound("footsteps")
                case "6": 
                    self.music.change_mode("aeolian")
                    self.ambient_sounds.change_sound("river")

                case "7": 
                    self.music.change_mode("locrian")
                    self.ambient_sounds.change_sound("dungeon")

                case "q":
                    # fade master volume
                    pass
                case _:
                    self.room_selection = input("Please enter a valid command: ")
            print(user_command)
            
main = Main()

s.gui(locals)