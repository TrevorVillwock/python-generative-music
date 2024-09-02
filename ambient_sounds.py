from pyo import SfPlayer, Fader
import os


"""
Ionian - Dining Hall
Dorian - Next to the river
Phrygian - Top of the tower
Lydian - Garden with birds
Mixolydian - Going for a hike
Aeolian - In the river
Locrian - Dungeon
"""
  
class AmbientSounds():
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.fader1 = Fader(fadein=2, fadeout=2)
        self.fader2 = Fader(fadein=2, fadeout=2)
        self.sound_sets = {"birds": [os.path.join(current_dir, "soundfiles", "ambient_sound", "birds.mp3")],
                       "dining_hall": [os.path.join(current_dir, "soundfiles", "ambient_sound", "dining_hall.mp3")], 
                       "dungeon": [os.path.join(current_dir, "soundfiles", "ambient_sound", "dungeon.mp3")],
                       "hike": [os.path.join(current_dir, "soundfiles", "ambient_sound", "footsteps.mp3"), os.path.join(current_dir, "soundfiles", "ambient_sound", "birds.mp3")],
                       "river": [os.path.join(current_dir, "soundfiles", "ambient_sound", "river.mp3")],
                       "underwater": [os.path.join(current_dir, "soundfiles", "ambient_sound", "underwater.mp3")],
                       "top_of_castle": [os.path.join(current_dir, "soundfiles", "ambient_sound", "rain.mp3"), os.path.join(current_dir, "soundfiles", "ambient_sound", "wind.mp3")]}
        self.sound_count = {"birds": 1, "dining_hall": 1, "dungeon": 1, "hike": 2, 
                            "river": 1, "underwater": 1, "top_of_castle": 2}
        self.sound_set_1 = [SfPlayer(self.sound_sets["birds"], loop=True, mul=self.fader1), SfPlayer(self.sound_sets["birds"], loop=True, mul=self.fader1), SfPlayer(self.sound_sets["birds"], loop=True, mul=self.fader1) ]
        self.sound_set_2 = [SfPlayer(self.sound_sets["dining_hall"], loop=True, mul=self.fader2), SfPlayer(self.sound_sets["dining_hall"], loop=True, mul=self.fader2), SfPlayer(self.sound_sets["dining_hall"], loop=True, mul=self.fader2)]
        self.current_sound_set = 1
        
    def play(self):
        self.current_sound_set[0].play()
        
    def change_sound(self, new_sound):
        # fade out old sounds and fade in new
        # print(new_sound)

        sounds_loaded = 0
        
        if self.current_sound_set == 1: 
            while sounds_loaded < self.sound_count[new_sound]:    
                self.sound_set_2[sounds_loaded].setPath(self.sound_sets[new_sound][sounds_loaded])
                self.sound_set_2[sounds_loaded].setMul(self.fader2)
                self.sound_set_2[sounds_loaded].out()
                sounds_loaded += 1
            while sounds_loaded < 3:
                self.sound_set_2[sounds_loaded].setMul(0)
                sounds_loaded += 1
            self.fader1.stop()
            self.fader2.play()
            self.current_sound_set = 2
            # print("if")
        else:
            while sounds_loaded < self.sound_count[new_sound]:
                self.sound_set_1[sounds_loaded].setPath(self.sound_sets[new_sound][sounds_loaded])
                self.sound_set_1[sounds_loaded].setMul(self.fader1)
                self.sound_set_1[sounds_loaded].out()
                sounds_loaded += 1
            while sounds_loaded < 3:
                self.sound_set_1[sounds_loaded].setMul(0)
                sounds_loaded += 1
            self.fader2.stop()
            self.fader1.play()
            self.current_sound_set = 1
            # print("else")
            
    def start_first_sound(self, first_sound):
        self.sound_set_1[0].setPath(self.sound_sets[first_sound])
        self.fader1.play()