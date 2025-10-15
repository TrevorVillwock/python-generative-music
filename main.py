from music import Music
from ambient_sounds import AmbientSounds
from pyo import Server, Mixer, Record, MoogLP, Selector
import sys
import time
import yaml

"""
TODO:
Add command to change delay times
Create other chord progressions
"""

s = Server().boot()
s.start()

class Main():  
    def __init__(self):
        self.input_is_valid = 1
        self.first_sound_started = 0
        self.music = Music("ionian") # default mode
        self.ambient_sounds = AmbientSounds()
        self.mixer = Mixer(outs=2, chnls=2, mul=0)
        self.filter = MoogLP(self.mixer[0], freq=1000)
        self.filter_selector = Selector([self.mixer[0], self.filter], voice=0).out()

        self.config = {}
        
        with open("config.yaml") as settings:
            try:
                self.config = yaml.safe_load(settings)
            except:
                print("error")
        
        print(self.config)
        print(self.config["recording_number"])
        
        # the file number is taken from config.yaml and incremented each time the program runs
        self.recorder = Record(self.mixer[0], filename=f"recording-{self.config['recording_number']}.wav")
        
        self.config['recording_number'] += 1
        
        with open("config.yaml", "w") as settings:
            try:
                yaml.dump({"recording_number": self.config['recording_number']}, settings)
            except:
                print("error")
        
        
        self.mixer.addInput(0, self.ambient_sounds.delay_selector)
        self.mixer.addInput(1, self.music.delay_selector)
        self.mixer.setAmp(0, 0, 0.5)
        self.mixer.setAmp(1, 0, 0.1)
        self.mixer.setTime(0.01)
        self.mixer.setMul(1)
        
        print("\n\nWelcome to CASTLE OF SOUND\n\n")
        print("""
What do you want to do?

1 - Eat breakfast (Ionian)
2 - Sit by the river (Dorian)
3 - Go to the top of the castle (Phrygian)
4 - Go to the garden (Lydian)
5 - Go for a hike (Mixolydian)
6 - Swim in the river (Aeolian)
7 - Go to the dungeon (Locrian)
e - Drink Essence of Bat
rt - Drink Elixir of Time
ge - Toggle guitar echo
time [seconds] - Change echo length
as - Toggle ambient sounds
f [frequency] - Change filter cutoff frequency
tf - Toggle filter
q - Quit """
              )
        self.action_selection = input("Input a number or letter to choose: ")
        self.action_selection_array = self.action_selection.split(' ')
        
        while True:
            print("\n", self.action_selection_array, "\n", len(self.action_selection_array), "\n")
            match self.action_selection_array[0]:
                case "1": 
                    # don't need to change modes since the default is ionian
                    self.input_is_valid = 1
                    if not self.first_sound_started:
                        self.ambient_sounds.start_first_sound("dining_hall")
                        self.first_sound_started = 1
                    else:
                        self.ambient_sounds.change_sound("dining_hall")
                        self.music.change_mode("ionian")
                        self.music.current_triad = 0    
                case "2":
                    self.input_is_valid = 1 
                    if not self.first_sound_started:
                        self.ambient_sounds.start_first_sound("river")
                        self.first_sound_started = 1
                    else:
                        self.ambient_sounds.change_sound("river")
                        self.music.change_mode("dorian")
                        self.music.current_triad = 0
                case "3": 
                    self.input_is_valid = 1
                    if not self.first_sound_started:
                        self.ambient_sounds.start_first_sound("top_of_castle")
                        self.first_sound_started = 1
                    else:
                        self.ambient_sounds.change_sound("top_of_castle")
                        self.music.change_mode("phrygian")
                        self.music.current_triad = 0
                case "4":
                    self.input_is_valid = 1
                    if not self.first_sound_started:
                        self.ambient_sounds.start_first_sound("birds")
                        self.first_sound_started = 1
                    else:
                        self.ambient_sounds.change_sound("birds")
                        self.music.change_mode("lydian")
                        self.music.current_triad = 0
                case "5":
                    self.input_is_valid = 1 
                    if not self.first_sound_started:
                        self.ambient_sounds.start_first_sound("hike")
                        self.first_sound_started = 1
                    else:
                        self.ambient_sounds.change_sound("hike")
                        self.music.change_mode("mixolydian")
                        self.music.current_triad = 0
                case "6":
                    self.input_is_valid = 1 
                    if not self.first_sound_started:
                        self.ambient_sounds.start_first_sound("underwater")
                        self.first_sound_started = 1
                    else:
                        self.ambient_sounds.change_sound("underwater")
                        self.music.change_mode("aeolian")
                        self.music.current_triad = 0
                case "7":
                    self.input_is_valid = 1 
                    if not self.first_sound_started:
                        self.ambient_sounds.start_first_sound("dungeon")
                        self.first_sound_started = 1
                    else:
                        self.ambient_sounds.change_sound("dungeon")
                        self.music.change_mode("locrian")
                        self.music.current_triad = 0
                case "rt":
                    self.input_is_valid = 1
                    self.music.reverse_samples()
                    self.ambient_sounds.reverse_sounds()
                case "e":
                    self.input_is_valid = 1
                    print("case e")
                    self.music.toggle_guitar_delay()
                    self.ambient_sounds.toggle_delay()
                case "ge":
                    self.input_is_valid = 1
                    self.music.toggle_guitar_delay()
                case "as":
                    self.input_is_valid = 1
                    self.ambient_sounds.volume_toggle()
                case "time":
                    self.input_is_valid = 1
                    delay = float(self.action_selection_array[1])
                    self.ambient_sounds.change_delay(delay)
                    self.music.change_guitar_delay(delay)
                case "v":
                    self.input_is_valid = 1
                    print("self.action_selection_array[1] != 'freq' or 'mult': " + str(self.action_selection_array[1] != "freq" or "mult"))
                    print("self.action_selection_array[1] != 'freq' and self.action_selection_array[1] != 'mult': " + str(self.action_selection_array[1] != "freq" and self.action_selection_array[1] !=  "mult"))
                    if len(self.action_selection_array) != 3 or (self.action_selection_array[1] != "freq" and self.action_selection_array[1] != "mult"):
                        print("Usage: v [freq or mult] [value]\nExample: v freq 0.1")
                    if self.action_selection_array[1] == "freq":
                        print("set freq")
                        self.music.pitch_lfo.setFreq(float(self.action_selection_array[2]))
                    elif self.action_selection_array[1] == "mult":
                        print("set mult")
                        self.music.pitch_lfo.setMul(float(self.action_selection_array[2]))
                case "q":
                    self.input_is_valid = 1
                    self.mixer.setMul(0.0)
                    self.music.stop()
                    self.ambient_sounds.stop()
                    print("\nFarewell!\n")
                    time.sleep(1)
                    s.shutdown()
                    sys.exit()
                case _:
                    self.input_is_valid = 0
                    self.action_selection = input("Please enter a valid command: ")
            
            if self.input_is_valid:        
                self.action_selection = input("Enter next command: ")
            self.action_selection_array = self.action_selection.split(' ')
                     
main = Main()
s.gui(locals)