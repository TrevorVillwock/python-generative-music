from music import Music
from ambient_sounds import AmbientSounds
from pyo import Server, Mixer, Record
import sys
import time

"""
TODO:
Add command to change delay times
Create other chord progressions
"""

s = Server().boot()
s.start()

class Main():  
    def __init__(self):
        self.input_is_valid = 0
        self.first_sound_started = 0
        self.music = Music("ionian") # default mode
        self.ambient_sounds = AmbientSounds()
        self.mixer = Mixer(outs=2, chnls=2, mul=0).out()
        
        # modify the filename here to make multiple recordings
        self.recorder = Record(self.mixer[0], filename="recording.wav")
        
        self.mixer.addInput(0, self.ambient_sounds.delay_selector)
        self.mixer.addInput(1, self.music.delay_selector)
        self.mixer.setAmp(0, 0, 0.5)
        self.mixer.setAmp(1, 0, 0.1)
        self.mixer.setTime(0.01)
        self.mixer.setMul(1)
        
        print("\n\nWelcome to CASTLE OF SOUND\n\n")
        print("What do you want to do?\n\n 1 - Eat breakfast (Ionian)\n 2 - Sit by the river (Dorian)\n 3 - Go to the top of the castle (Phrygian)\n 4 - Go to the garden (Lydian)\n 5 - Go for a hike (Mixolydian) \n 6 - Swim in the river (Aeolian) \n 7 - Go to the dungeon (Locrian)\n e - Drink Essence of Bat\n rt - Drink Elixir of Time \n ge - Toggle guitar echo\n time - Change echo length\n as - Toggle ambient sounds\n q - Quit \n\n")
        self.action_selection = input("Input a number or letter to choose: ")
        self.action_selection_array = self.action_selection.split(' ')
        
        while True:
            print("\n")
            match self.action_selection_array[0]:
                case "1": 
                    # don't need to change modes since the default is ionian
                    if not self.first_sound_started:
                        self.ambient_sounds.start_first_sound("dining_hall")
                        self.first_sound_started = 1
                    else:
                        self.ambient_sounds.change_sound("dining_hall")
                        self.music.change_mode("ionian")
                        self.music.current_triad = 0    
                case "2": 
                    if not self.first_sound_started:
                        self.ambient_sounds.start_first_sound("river")
                        self.first_sound_started = 1
                    else:
                        self.ambient_sounds.change_sound("river")
                        self.music.change_mode("dorian")
                        self.music.current_triad = 0
                case "3": 
                    if not self.first_sound_started:
                        self.ambient_sounds.start_first_sound("top_of_castle")
                        self.first_sound_started = 1
                    else:
                        self.ambient_sounds.change_sound("top_of_castle")
                        self.music.change_mode("phrygian")
                        self.music.current_triad = 0
                case "4":
                    if not self.first_sound_started:
                        self.ambient_sounds.start_first_sound("birds")
                        self.first_sound_started = 1
                    else:
                        self.ambient_sounds.change_sound("birds")
                        self.music.change_mode("lydian")
                        self.music.current_triad = 0
                case "5": 
                    if not self.first_sound_started:
                        self.ambient_sounds.start_first_sound("hike")
                        self.first_sound_started = 1
                    else:
                        self.ambient_sounds.change_sound("hike")
                        self.music.change_mode("mixolydian")
                        self.music.current_triad = 0
                case "6": 
                    if not self.first_sound_started:
                        self.ambient_sounds.start_first_sound("underwater")
                        self.first_sound_started = 1
                    else:
                        self.ambient_sounds.change_sound("underwater")
                        self.music.change_mode("aeolian")
                        self.music.current_triad = 0
                case "7": 
                    if not self.first_sound_started:
                        self.ambient_sounds.start_first_sound("dungeon")
                        self.first_sound_started = 1
                    else:
                        self.ambient_sounds.change_sound("dungeon")
                        self.music.change_mode("locrian")
                        self.music.current_triad = 0
                case "rt":
                    self.music.reverse_samples()
                    self.ambient_sounds.reverse_sounds()
                case "e":
                    print("case e")
                    self.music.toggle_guitar_delay()
                    self.ambient_sounds.toggle_delay()
                case "ge":
                    self.music.toggle_guitar_delay()
                case "as":
                    self.ambient_sounds.volume_toggle()
                case "time":
                    delay = float(self.action_selection_array[1])
                    self.ambient_sounds.change_delay(delay)
                    self.music.change_guitar_delay(delay)
                case "q":
                    self.mixer.setMul(0.0)
                    self.music.stop()
                    self.ambient_sounds.stop()
                    print("\nFarewell!\n")
                    time.sleep(1)
                    s.shutdown()
                    sys.exit()
                case _:
                    self.action_selection = input("Please enter a number between 1 and 7: ")
                    
            self.action_selection = input("Enter next command: ")
            self.action_selection_array = self.action_selection.split(' ')
            
main = Main()

s.gui(locals)