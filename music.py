"""
    TODO
    Imitation
    Control interval of harmonization
    Counterpoint
    Instruments you can play from the command line
"""

from pyo import *
from math import floor

class Music():
    def __init__(self, mode):
        self.melody_met = Metro(0.5).play()
        self.bass_met = Metro(2).play()
        self.modes = {"Ionian": [0, 2, 4, 5, 7, 9, 11, 12, 
                                 14, 16, 17, 19, 21, 23, 24],
                      "Dorian": [0, 2, 3, 5, 7, 9, 10, 12, 
                                 14, 15, 17, 19, 21, 22, 24],
                      "Phrygian": [0, 1, 3, 5, 7, 8, 10, 12, 
                                   13, 15, 17, 19, 20, 22, 24],
                      "Lydian": [0, 2, 4, 6, 7, 9, 11, 12, 
                                 14, 16, 18, 19, 21, 23, 24],
                      "Mixolydian": [0, 2, 4, 5, 7, 9, 11, 12, 
                                     14, 16, 17, 19, 21, 22, 24],
                      "Aeolian": [0, 2, 3, 5, 7, 8, 10, 12, 
                                  14, 15, 17, 19, 20, 22, 24],
                      "Locrian": [0, 1, 3, 5, 7, 8, 10, 12, 
                                  13, 15, 17, 19, 20, 22, 24]}
        self.current_mode = self.modes[mode]
        
        # amplitude (volume) envelopes
        # these control how the sounds start and stop
        # Attack Decay Sustain Release
        # Attack - how long the sound takes to start (seconds)
        # Decay - how long the sound takes to reach sustain volume from max (seconds)
        # Sustain - volume level when note is held (volume from 0.0-1.0)
        # Release - how long the note takes to fade away
        self.melody_env = Adsr(0.1, dur=0.25)
        self.bass_env = Adsr(0.1, release=1, dur=2)

        # each note of the motif is represented as an array containing the scale degree and duration in seconds
        # 1 = quarter note, 0.5 = eighth, etc.
        self.motifs = [[[5, 0.5], [5, 0.25], [5, 0.25], [3, 0.5]], 
                       [[4, 0.25], [4, 0.5], [4, 0.25], [2, 1]]]

        # [1, 3, 2, 4], [5, 5, 5, 7, 6], [1, 2, 6, 4]
        self.playing_motif = False
        self.use_motif = 0
        self.motif_num = 0
        self.motif_step = 0

        # Square waveform generator using first 5 odd harmonics
        self.melody_wav = SquareTable(5)
        self.bass_wav = SquareTable(5)

        # self.melody_synth = Osc(table=self.melody_wav, freq=[midiToHz(60), midiToHz(60)], mul=self.melody_env)
        self.melody_note = 60
        # self.harmonizing_synth = Osc(table=self.melody_wav, freq=[midiToHz(60), midiToHz(60)], mul=self.melody_env)
        self.harmony_note = 57
        # self.bass_synth = Osc(table=self.bass_wav, freq=[midiToHz(36), midiToHz(36)], mul=self.bass_env)
        self.bass_note = 28
        
        self.melody_vol = 0.3
        self.harmony_vol = 0.3
        
        self.notes_to_harmonize = 0
        
        # self.melody_reverb = Freeverb(self.melody_synth, 2)
        # self.harmony_reverb = Freeverb(self.harmonizing_synth, 2)

        self.mixer = Mixer(chnls=4)

        # self.mixer.addInput(0, self.melody_reverb)
        # self.mixer.addInput(1, self.harmony_reverb)
        # self.mixer.addInput(2, self.bass_synth)

        # self.mixer.setAmp(0, 0, 0.1)
        # self.mixer.setAmp(1, 0, 0.1)
        # self.mixer.setAmp(2, 0, 0.1)
        
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
        self.bass_player = TrigFunc(self.bass_met, self.play_bass)

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
                # self.melody_synth.setFreq(midiToHz(60 + self.current_mode[self.motifs[self.motif_num][self.motif_step][0] - 1]))
                self.melody_note = 60 + self.current_mode[self.motifs[self.motif_num][self.motif_step][0] - 1]
                # self.harmonizing_synth.setFreq(midiToHz(60 + self.current_mode[(self.motifs[self.motif_num][self.motif_step][0] + 1) % 13]))
                self.harmony_note = 60 + self.current_mode[(self.motifs[self.motif_num][self.motif_step][0] + 1) % 13]
                
                # Below and is an alternate method of specifying an interval to harmonize the melody at; it's also at line 143.
                # When harmonizing the melody in 3rds using scale degrees, the interval  
                # between the two voices changes between major and minor thirds depending on which scale degrees
                # are involved. By multiplying the melody note's frequency by a fraction representing the interval of harmonization,
                # however, we can get the same interval every time. This also makes it very easy to play with notes from
                # the harmonic series that are in what's called "just intonation."
                #
                # The notes on a piano keyboard are all the same interval apart; every half step sounds the same to us.
                # However, many different tuning systems have been used across time and in different places in the world. 
                # Some are based on more "pure" or "just" intervals because which use simple
                # whole number ratios for intervals like the perfect 5th (3/2 or 1.5) and the major third (5/4 or 1.25). The major third on
                # a piano by contrast has the interval ratio of 1.259921, meaning the top note is slightly sharp compared to the just interval.
                
                # for a great explanation of these concepts, check out this video: https://youtu.be/Wx_kugSemfY?si=SxQimSSkHc5A6B2H

                # self.harmonizing_synth.setFreq(7/4 * midiToHz(60 + scale[self.motifs[self.motif_num][self.motif_step] - 1]))
                self.melody_met.setTime(self.motifs[self.motif_num][self.motif_step][1])
                self.motif_step += 1
            else:
                # self.melody_synth.setFreq(midiToHz(60 + self.current_mode[self.motifs[self.motif_num][self.motif_step][0] - 1]))
                self.melody_note = 60 + self.current_mode[self.motifs[self.motif_num][self.motif_step][0] - 1]
                # self.harmonizing_synth.setFreq(midiToHz(60 + self.current_mode[(self.motifs[self.motif_num][self.motif_step][0] + 1) % 13]))
                self.harmony_note = 60 + self.current_mode[self.motifs[self.motif_num][self.motif_step][0] - 1]
                self.melody_met.setTime(self.motifs[self.motif_num][self.motif_step][1])
                self.motif_step = 0
                self.playing_motif = False
        else:
            # random_degree = random.randint(0, 7)
            random_degree = random.randrange(0, 23)
            # self.melody_synth.setFreq(midiToHz(60 + self.current_mode[random_degree]))
            self.melody_note = self.midi_numbers[random_degree]
            # self.harmonizing_synth.setFreq(midiToHz(60 + self.current_mode[(random_degree + 2) % 13]))
            self.harmony_note = self.midi_numbers[random_degree - 2]
            
            # self.harmonizing_synth.setFreq(7/4 * midiToHz(60 + scale[random_degree]))

        # print(f"notes_to_harmonize: {notes_to_harmonize}")
        if self.notes_to_harmonize == 0:
            harmonize = random.random()
            if harmonize > 0.5:
                self.notes_to_harmonize = 3 + random.randint(0, 5)
        
        if change_rhythm > 0.5 and not self.playing_motif:
            self.melody_met.setTime(new_rhythm)
        
        # 0 = staccato, 1 = legato
        current_articulation = round(random.random())
        if current_articulation == 1:
            # if legato, make duration of envelope same as note length
            self.melody_env.setDur(new_rhythm)
        else:
            self.melody_env.setDur(0.25)
            
        if self.notes_to_harmonize != 0:
            # self.harmonizing_synth.setMul(self.melody_env)
            self.harmony_vol = self.melody_vol
            self.notes_to_harmonize -= 1
        else:
            # self.harmonizing_synth.setMul(0)
            self.harmony_vol = 0
          
        if play_note > 0.3:
            # self.melody_env.play()
            self.play_guitar(self.melody_note)
            self.play_guitar(self.harmony_note)
            # print("playing melody")
            pass

    def play_bass(self):
        # print("play_bass")
        change_note = random.random()
        if change_note > 0.3:
            # print("playing bass")
            # self.bass_synth.setFreq(midiToHz(36 + self.current_mode[random.randint(0, 7)]))
            self.bass_note = self.midi_numbers[random.randint(0, 7)]
        # self.bass_env.play()
        self.play_guitar(self.bass_note)
        
    def play_guitar(self, note):
        self.guitar_samples[note][0].out()
        print(note)  