from pyo import SfPlayer

"""
Ionian - Dining Hall
Dorian - Next to the river
Phrygian - Top of the tower - wind
Lydian - Garden with birds
Mixolydian - Stables (muddy footsteps, horses)
Aeolian - In the river
Locrian - Dungeon (under metallic floor)
"""

class AmbientNoise():
    def __init__(self):
        self.noise = SfPlayer("./soundfiles/ambient_noise/birds.mp3", loop=True).out()
        
    def play(self):
        self.noise.play()