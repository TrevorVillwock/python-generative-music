from music import Music
from ambient_noise import AmbientNoise
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
                    self.mode = "Ionian"
                    self.input_is_valid = 1
                case "2": 
                    self.mode = "Dorian"
                    self.input_is_valid = 1
                case "3": 
                    self.mode = "Phrygian"
                    self.input_is_valid = 1
                case "4": 
                    self.mode = "Lydian"
                    self.input_is_valid = 1
                case "5": 
                    self.mode = "Mixolydian"
                    self.input_is_valid = 1
                case "6": 
                    self.mode = "Aeolian"
                    self.input_is_valid = 1
                case "7": 
                    self.mode = "Locrian"
                    self.input_is_valid = 1
                case _:
                    self.room_selection = input("Please enter a number between 1 and 7:")
        
        self.music = Music(self.mode)
        self.ambient_noise = AmbientNoise()
        self.mixer = Mixer(chnls=2).out()
        
        # self.mixer.addInput(0, self.music.melody_reverb)
        # self.mixer.addInput(1, self.music.harmony_reverb)
        # self.mixer.addInput(2, self.music.bass_synth)
        self.mixer.addInput(3, self.ambient_noise.noise)

        self.mixer.setAmp(0, 0, 0.1)
        self.mixer.setAmp(1, 0, 0.1)
        self.mixer.setAmp(2, 0, 0.1)
        self.mixer.setAmp(3, 0, 0.3)

main = Main()

s.gui(locals)
