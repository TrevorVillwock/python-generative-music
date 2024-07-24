from soundtrack import Soundtrack
from pyo import *

s = Server().boot()
s.start()

class Main():  
    def __init__(self):
        self.input_is_valid = 0
        self.mode = "Ionian" # default mode
        self.room_selection = input("Input a number to enter the cooresponding room:\n\n 1. Ionian\n 2. Dorian\n 3. Phrygian\n 4. Lydian\n 5. Mixolydian\n 6. Aeolian\n 7. Locrian\n\n")
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
        self.soundtrack = Soundtrack(self.mode)

main = Main()

s.gui(locals)
