from pyo import Metro, SfPlayer, Mixer, TrigFunc
import random
from math import floor

"""
Create dictionary mapping modes to primary triads
Create new current_mode_name attribute?
    
"""
class Music():
    def __init__(self, mode):
        self.melody_met = Metro(0.5).play()
        self.bass_met = Metro(2).play()
        self.chord_met = Metro(2).play()
        self.modes = {"ionian": [0, 2, 4, 5, 7, 9, 11, 12, 
                                 14, 16, 17, 19, 21, 23, 24],
                      "dorian": [0, 2, 3, 5, 7, 9, 10, 12, 
                                 14, 15, 17, 19, 21, 22, 24],
                      "phrygian": [0, 1, 3, 5, 7, 8, 10, 12, 
                                   13, 15, 17, 19, 20, 22, 24],
                      "lydian": [0, 2, 4, 6, 7, 9, 11, 12, 
                                 14, 16, 18, 19, 21, 23, 24],
                      "mixolydian": [0, 2, 4, 5, 7, 9, 11, 12, 
                                     14, 16, 17, 19, 21, 22, 24],
                      "aeolian": [0, 2, 3, 5, 7, 8, 10, 12, 
                                  14, 15, 17, 19, 20, 22, 24],
                      "locrian": [0, 1, 3, 5, 7, 8, 10, 12, 
                                  13, 15, 17, 19, 20, 22, 24]}
        
        self.current_mode = self.modes[mode]
        
        self.current_mode_name = mode
        
        # Simple progressions using the primary triads (I, IV, and V) in each mode.
        # The I chord is repeated to help establish the mode and we use open voicings to make
        # the chords more full and less muddy in the low registers. To make an open voicing, we
        # move the middle note of the triad up an octave by adding 12 to the original midi number.
        
        self.mode_primary_triads = {"ionian": [[31, 47, 38], [31, 47, 38], [36, 52, 43], [38, 54, 45]],
                      "dorian": [[33, 48, 40], [33, 48, 40], [38, 54, 45], [40, 55, 47]],
                      "phrygian": [[35, 50, 42], [35, 50, 42], [40, 55, 47], [42, 57, 48]],
                      "lydian": [[36, 52, 43], [36, 52, 43], [42, 57, 48], [43, 59, 50]],
                      "mixolydian": [[38, 54, 45], [38, 54, 45], [43, 59, 50], [45, 60, 52]],
                      "aeolian": [[28, 43, 35], [28, 43, 35], [33, 48, 40], [35, 50, 42]],
                      "locrian": [[30, 45, 36], [30, 45, 36], [35, 50, 42], [36, 52, 43]]}
        
        self.current_triad = 0

        # each note of the motif is represented as an array containing the scale degree and duration in seconds
        # 1 = quarter note, 0.5 = eighth, etc.
        self.motifs = [[[5, 0.5], [5, 0.25], [5, 0.25], [3, 0.5]], 
                       [[4, 0.25], [4, 0.5], [4, 0.25], [2, 1]]]

        self.playing_motif = False
        self.use_motif = 0
        self.motif_num = 0
        self.motif_step = 0

        self.melody_note = 60
        self.harmony_note = 57
        self.bass_note = 28
        
        self.melody_vol = 0.3
        self.harmony_vol = 0.3
        
        self.notes_to_harmonize = 0

        self.mixer = Mixer(chnls=4)
        
        # create a dictionary where each key is a midi number and each value is an array containing that note at all possible dynamics
        # randomly select dynamic to play
        self.guitar_samples = {}
        self.midi_numbers = [28, 30, 31, 33, 35, 36, 38, 40, 42, 43, 45, 47, 48, 50, 52, 54, 55, 57, 59, 60, 62, 64, 66, 69]
        for m in self.midi_numbers:
            self.guitar_samples[m] = []
            for i in range (1, 6):
                try:
                    self.guitar_samples[m].append(SfPlayer(f"soundfiles/guitar_samples/{m}-{i}.aif"))
                except Exception as e:
                    pass
                    # print("exception: " + str(e))
                    
        self.melody_player = TrigFunc(self.melody_met, self.play_melody)
        # self.bass_player = TrigFunc(self.bass_met, self.play_bass)
        self.chord_player = TrigFunc(self.chord_met, self.play_chords)

    def play_melody(self):
        # print("play_melody")
        play_note = random.random()
        change_rhythm = random.random()
        new_rhythm = random.choice([0.25, 0.5, 0.75, 1])   
        modify_motif_pitch = random.random()
        modify_motif_rhythm = random.random()
        
        if not self.playing_motif:
            self.use_motif = random.random()
            self.motif_num = round(random.random())
        
        if self.use_motif > 1:
            self.playing_motif = True
            
        if self.playing_motif:
            if modify_motif_pitch > 0.8:
                # print(f"old motif pitches: {self.motifs[self.motif_num]}")
                note_to_change = floor(random.random() * 4)
                change_interval = random.choice([-1, 1])
                self.motifs[self.motif_num][note_to_change][0] = self.motifs[self.motif_num][note_to_change][0] + change_interval
                # print(f"new motif pitches: {self.motifs[self.motif_num]}")
                
            if modify_motif_rhythm > 0.8:
                # print(f"old motif rhythm: {self.motifs[self.motif_num]}")
                note_to_change = floor(random.random() * 4)
                self.motifs[self.motif_num][note_to_change][1] = random.choice([r for r in [0.25, 0.5, 0.75, 1] if r != self.motifs[self.motif_num][note_to_change][1]])
                # print(f"new motif rhythm: {self.motifs[self.motif_num]}")
                
            play_note = 1 # make sure no notes of the motif are replaced with rests
            if self.motif_step < len(self.motifs[self.motif_num]) - 1:
                # scale[self.motifs[self.motif_num][self.motif_step] - 1] gives the number of half steps above middle C
                # print(f"motif {self.motif_num}, self.motif_step {self.motif_step}, motif degree: {self.motifs[self.motif_num][self.motif_step]}, scale_note: {self.current_mode[self.motifs[self.motif_num][self.motif_step][0] - 1]}")
                self.melody_note = 60 + self.current_mode[self.motifs[self.motif_num][self.motif_step][0] - 1]
                self.harmony_note = 60 + self.current_mode[(self.motifs[self.motif_num][self.motif_step][0] + 1) % 13]
                self.melody_met.setTime(self.motifs[self.motif_num][self.motif_step][1])
                self.motif_step += 1
            else:
                self.melody_note = 60 + self.current_mode[self.motifs[self.motif_num][self.motif_step][0] - 1]
                self.harmony_note = 60 + self.current_mode[self.motifs[self.motif_num][self.motif_step][0] - 1]
                self.melody_met.setTime(self.motifs[self.motif_num][self.motif_step][1])
                self.motif_step = 0
                self.playing_motif = False
        else:
            random_degree = random.randint(0, 23)
            self.melody_note = self.midi_numbers[random_degree]
            self.harmony_note = self.midi_numbers[random_degree - 2]

        # print(f"notes_to_harmonize: {notes_to_harmonize}")
        if self.notes_to_harmonize == 0:
            harmonize = random.random()
            if harmonize > 0.5:
                self.notes_to_harmonize = 3 + random.randint(0, 5)
        
        if change_rhythm > 0.5 and not self.playing_motif:
            self.melody_met.setTime(new_rhythm)
            
        if self.notes_to_harmonize != 0:
            self.harmony_vol = self.melody_vol
            self.notes_to_harmonize -= 1
        else:
            self.harmony_vol = 0
          
        if play_note > 0.3:
            self.play_guitar(self.melody_note)
            self.play_guitar(self.harmony_note)
            # print("playing melody")

    def play_chords(self):
        # print(f"self.current_triad: {self.current_triad}")
        self.play_guitar(self.mode_primary_triads[self.current_mode_name][self.current_triad][0])
        self.play_guitar(self.mode_primary_triads[self.current_mode_name][self.current_triad][1])
        self.play_guitar(self.mode_primary_triads[self.current_mode_name][self.current_triad][2])
        
        if self.current_triad < 3:
            self.current_triad += 1
        else:
            self.current_triad = 0
            
    def play_bass(self):
        # print("play_bass")
        change_note = random.random()
        if change_note > 0.3:
            self.bass_note = self.midi_numbers[random.randint(0, 7)]
        self.play_guitar(self.bass_note)
        
    def play_guitar(self, note):
        self.guitar_samples[note][0].out()
        # print(note)  
        
    def change_mode(self, mode):
        self.current_mode_name = mode
        self.current_mode = self.modes[mode]
        