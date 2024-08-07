from pyo import SfPlayer, Fader

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
        self.fader1 = Fader(fadein=2, fadeout=2)
        self.fader2 = Fader(fadein=2, fadeout=2)
        self.sounds = {"birds": "./soundfiles/ambient_sound/birds.mp3",
                       "dining_hall": "./soundfiles/ambient_sound/dining_hall.mp3", 
                       "dungeon": "./soundfiles/ambient_sound/dungeon.mp3",
                       "footsteps": "./soundfiles/ambient_sound/footsteps.mp3",
                       "river": "./soundfiles/ambient_sound/river.mp3",
                       "underwater": "./soundfiles/ambient_sound/underwater.mp3",
                       "wind": "./soundfiles/ambient_sound/wind.mp3"}
        self.sound1 = SfPlayer(self.sounds["birds"], loop=True, mul=self.fader1)
        self.sound2 = SfPlayer(self.sounds["dining_hall"], loop=True, mul=self.fader2)
        self.current_sound = 1
        
    def play(self):
        self.current_sound.play()
        
    def change_sound(self, new_sound):
        # fade out old sound and fade in new
        # print(new_sound)
        if self.current_sound == 1:
            self.sound2.setPath(self.sounds[new_sound])
            self.fader1.stop()
            self.sound2.out()
            self.fader2.play()
            self.current_sound = 2
            # print("if")
        else:
            self.sound1.setPath(self.sounds[new_sound])
            self.fader2.stop()
            self.sound1.play()
            self.fader1.play()
            self.current_sound = 1
            # print("else")
            
    def start_first_sound(self, first_sound):
        self.sound1.setPath(self.sounds[first_sound])
        self.fader1.play()