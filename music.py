from pyo import Metro, SfPlayer, Mixer, TrigFunc
import random
from math import floor

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
        self.harmonizing = False
        self.bass_note = 28
        
        self.melody_vol = 0.3
        self.harmony_vol = 0.3
        
        self.notes_to_harmonize = 0

        self.mixer = Mixer(chnls=4).out()
        
        # Below we create a dictionary where each key is a midi number and each value
        # is an array containing that note at all possible dynamics.
        
        # At the moment we're only using the lowest dynamic to simplify things
        # but later we'll randomly select a dynamic to play as well make it possible
        # to control crescendos and diminuendos.
        
        self.guitar_samples = {}
        self.midi_numbers = [28, 30, 31, 33, 35, 36, 38, 40, 42, 43, 45, 47, 48, 
                             50, 52, 54, 55, 57, 59, 60, 62, 64, 66, 69]
        
        self.guitar_mixer = Mixer(chnls=100, mul=0.5).out()
        
        # this will be incremented every time we add a guitar sample to the mixer to provide the channel number 
        self.guitar_channel = 0
        
        for m in self.midi_numbers:
            # We make the first element of the array None so that the number of the guitar sample
            # (i.e. the 1 in 28-1) aligns with its index in the list
            self.guitar_samples[m] = SfPlayer(f"soundfiles/guitar_samples/{m}-1.aif").stop()
            # self.guitar_mixer.addInput(self.guitar_channel, self.guitar_samples[m][i])
            self.guitar_mixer.addInput(self.guitar_channel, self.guitar_samples[m])
            self.guitar_mixer.setAmp(self.guitar_channel, 0, 0.1)
            print(f"self.guitar_channel: {self.guitar_channel}")
            self.guitar_channel += 1
        
        # attempt below to add all velocities for every note
        # for m in self.midi_numbers:
        #     # We make the first element of the array None so that the number of the guitar sample
        #     # (i.e. the 1 in 28-1) aligns with its index in the list
        #     self.guitar_samples[m] = []
        #     self.guitar_samples[m].append(None)
        #     print(f"m: {m}")
        #     for i in range (1, 6):
        #         print(f"i: {i}")
        #         try:
        #             # the array here makes it so that the mono guitar sample will play in stereo;
        #             # two elements are inputs for the left and right channels
        #             # self.guitar_samples[m].append(SfPlayer([f"soundfiles/guitar_samples/{m}-{i}.aif", f"soundfiles/guitar_samples/{m}-{i}.aif"]))
        #             self.guitar_samples[m].append(SfPlayer(f"soundfiles/guitar_samples/{m}-{i}.aif").stop())
        #             # self.guitar_mixer.addInput(self.guitar_channel, self.guitar_samples[m][i])
        #             self.guitar_mixer.addInput(self.guitar_channel, self.guitar_samples[m][i])
        #             self.guitar_mixer.setAmp(self.guitar_channel, 0, 0.01)
        #             print(f"self.guitar_channel: {self.guitar_channel}")
        #             self.guitar_channel += 1
        #         except Exception as e:
        #             pass
        #             # self.guitar_samples[m].append(None)
        #             # We do this because different notes have different numbers of samples; some are sampled
        #             # at 5 dynamic levels while others have only 2 or 3. 
        #             # Uncomment the line below to see the exception message.
                    
        #             # print("exception: " + str(e))
                             
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
        
        # if we're not already playing a motif, randomly 
        # determine if we'll start one on the next note
        if not self.playing_motif:
            self.use_motif = random.random()
            self.motif_num = round(random.random())
        
        if self.use_motif > 0.3:
            self.playing_motif = True
            
        if self.playing_motif:
            if modify_motif_pitch > 0.5:
                # print(f"old motif pitches: {self.motifs[self.motif_num]}")
                note_to_change = floor(random.random() * 4)
                change_interval = random.choice([-1, 1])
                
                # pitch is the first number in the motif array so we access it with [0]
                self.motifs[self.motif_num][note_to_change][0] = self.motifs[self.motif_num][note_to_change][0] + change_interval
                # print(f"new motif pitches: {self.motifs[self.motif_num]}")
                
            if modify_motif_rhythm > 0.5:
                # print(f"old motif rhythm: {self.motifs[self.motif_num]}")
                note_to_change = floor(random.random() * 4)
                
                # rhythm is the second number in the motif array so we access it with [1]
                self.motifs[self.motif_num][note_to_change][1] = random.choice([r for r in [0.25, 0.5, 0.75, 1] if r != self.motifs[self.motif_num][note_to_change][1]])
                # print(f"new motif rhythm: {self.motifs[self.motif_num]}")
                
            play_note = 1 # make sure no notes of the motif are replaced with rests
            if self.motif_step < len(self.motifs[self.motif_num]) - 1:
                # scale[self.motifs[self.motif_num][self.motif_step] - 1] gives the number of half steps above middle C
                # print(f"motif {self.motif_num}, self.motif_step {self.motif_step}, motif degree: {self.motifs[self.motif_num][self.motif_step]}, scale_note: {self.current_mode[self.motifs[self.motif_num][self.motif_step][0] - 1]}")
                
                self.melody_note = self.midi_numbers[8 + self.motifs[self.motif_num][self.motif_step][0]]
                
                self.harmony_note = self.midi_numbers[10 + self.motifs[self.motif_num][self.motif_step][0]]
                self.melody_met.setTime(self.motifs[self.motif_num][self.motif_step][1])
                self.motif_step += 1
            else:
                self.melody_note = self.midi_numbers[8 + self.motifs[self.motif_num][self.motif_step][0]]
                self.harmony_note = self.midi_numbers[10 + self.motifs[self.motif_num][self.motif_step][0]]
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
            if harmonize > 0.8:
                self.harmonizing = True
                self.notes_to_harmonize = 3 + random.randint(0, 5)
            else:
                self.harmonizing = False
        
        if change_rhythm > 0.5 and not self.playing_motif:
            self.melody_met.setTime(new_rhythm)
            
        if self.notes_to_harmonize != 0:
            self.notes_to_harmonize -= 1
          
        if play_note > 0.3:
            self.play_guitar(self.melody_note)
            if self.harmonizing:   
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
        self.guitar_samples[note].play()
        # print(self.guitar_samples[note][1].path)
        # print(note)  
        
    def change_mode(self, mode):
        self.current_mode_name = mode
        self.current_mode = self.modes[mode]
        
    def stop(self):
        self.melody_met.stop()
        self.chord_met.stop()
        self.bass_met.stop()