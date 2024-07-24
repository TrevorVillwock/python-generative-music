"""
    TODO
    Motivic development
    Imitation
    Control interval of harmonization
    Counterpoint
    Improve timbre
    Add soundfile playback - footsteps, dripping, birds, wind, conversation
    Create command line choose your own adventure type thing with different rooms for different modes, instruments you can play, and other objects/controls that change the soundtrack
    Instruments you can play from the command line
"""

from pyo import *

s = Server().boot()
s.start()

class Soundtrack():
    def __init__(self, mode):
        self.melody_met = Metro(0.5).play()
        self.bass_met = Metro(2).play()
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

        self.melody_synth = Osc(table=self.melody_wav, freq=[midiToHz(60), midiToHz(60)], mul=self.melody_env)
        self.harmonizing_synth = Osc(table=self.melody_wav, freq=[midiToHz(60), midiToHz(60)], mul=self.melody_env)
        self.notes_to_harmonize = 0
        self.bass_synth = Osc(table=self.bass_wav, freq=[midiToHz(36), midiToHz(36)], mul=self.bass_env)

        self.melody_reverb = Freeverb(self.melody_synth, 2)
        self.harmony_reverb = Freeverb(self.harmonizing_synth, 2)

        self.melody_player = TrigFunc(self.melody_met, self.play_melody)
        self.bass_player = TrigFunc(self.bass_met, self.play_bass)

        self.mixer = Mixer(chnls=4).out()

        self.mixer.addInput(0, self.melody_reverb)
        self.mixer.addInput(1, self.harmony_reverb)
        self.mixer.addInput(2, self.bass_synth)

        self.mixer.setAmp(0, 0, 0.1)
        self.mixer.setAmp(1, 0, 0.1)
        self.mixer.setAmp(2, 0, 0.1)

    def play_melody(self):
        # print("play_melody")
        play_note = random.random()
        change_rhythm = random.random()
        new_rhythm = random.choice([0.25, 0.5, 0.75, 1])
        
        if not self.playing_motif:
            self.use_motif = random.random()
            self.motif_num = round(random.random())
        
        if self.use_motif > 0.4:
            self.playing_motif = True
            
        if self.playing_motif:
            play_note = 1 # make sure no notes of the motif are replaced with rests
            if self.motif_step < len(self.motifs[self.motif_num]) - 1:
                # scale[self.motifs[self.motif_num][self.motif_step] - 1] gives the number of half steps above middle C
                # print(f"motif {self.motif_num}, self.motif_step {self.motif_step}, motif degree: {self.motifs[self.motif_num][self.motif_step]}, scale_note: {self.current_mode[self.motifs[self.motif_num][self.motif_step][0] - 1]}")
                self.melody_synth.setFreq(midiToHz(60 + self.current_mode[self.motifs[self.motif_num][self.motif_step][0] - 1]))
                self.harmonizing_synth.setFreq(midiToHz(60 + self.current_mode[(self.motifs[self.motif_num][self.motif_step][0] + 1) % 13]))
                
                # Below and is an alternate method of specifying an interval to harmonize the melody at; it's also at line 143.
                # When harmonizing the melody in 3rds using scale degrees, the interval  
                # between the two voices changes between major and minor thirds depending on which scale degrees
                # are involved. By multiplying the melody note's frequency by a fraction representing the interval of harmonization,
                # however, we can get the same interval every time. This also makes it very easy to play with notes from
                # the harmonic series that are in what's called "just intonation."
                #
                # The notes on a piano keyboard are all the same interval apart; every half step sounds the same to us.
                # However, many different tuning systems have been used across time and in different places in the world. 
                # Some are based on more "pure" or "just" intervals because they use simple
                # whole number ratios for intervals like the perfect 5th (3/2 or 1.5) and the major third (5/4 or 1.25). The major third on
                # a piano by contrast has the interval ratio of 1.259921, meaning the top note is slightly sharp compared to the just interval.
                
                # for a great explanation of these concepts, check out this video: https://youtu.be/Wx_kugSemfY?si=SxQimSSkHc5A6B2H

                # self.harmonizing_synth.setFreq(7/4 * midiToHz(60 + scale[self.motifs[self.motif_num][self.motif_step] - 1]))
                self.melody_met.setTime(self.motifs[self.motif_num][self.motif_step][1])
                self.motif_step += 1
                print(f"setting time to {self.motifs[self.motif_num][self.motif_step][1]}")
            else:
                print(f"motif {self.motif_num}, self.motif_step {self.motif_step}, motif degree: {self.motifs[self.motif_num][self.motif_step]}, scale_note: {self.current_mode[self.motifs[self.motif_num][self.motif_step][0] - 1]}")
                self.melody_synth.setFreq(midiToHz(60 + self.current_mode[self.motifs[self.motif_num][self.motif_step][0] - 1]))
                
                self.harmonizing_synth.setFreq(midiToHz(60 + self.current_mode[(self.motifs[self.motif_num][self.motif_step][0] + 1) % 13]))
                self.melody_met.setTime(self.motifs[self.motif_num][self.motif_step][1])
                self.motif_step = 0
                self.playing_motif = False
        else:
            random_degree = random.randint(0, 7)
            self.melody_synth.setFreq(midiToHz(60 + self.current_mode[random_degree]))
            self.harmonizing_synth.setFreq(midiToHz(60 + self.current_mode[(random_degree + 2) % 13]))
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
            self.harmonizing_synth.setMul(self.melody_env)
            self.notes_to_harmonize -= 1
        else:
            self.harmonizing_synth.setMul(0)
          
        if play_note > 0.3:
            self.melody_env.play()
            # print("playing melody")

    def play_bass(self):
        # print("play_bass")
        change_note = random.random()
        if change_note > 0.3:
            # print("playing bass")
            self.bass_synth.setFreq(midiToHz(36 + self.current_mode[random.randint(0, 7)]))
        self.bass_env.play()

soundtrack1 = Soundtrack("dorian")

s.gui(locals)