from pyo import Metro, SfPlayer, Mixer, TrigFunc, Delay, Selector, Sine, Adsr, STRev, Disto, Fader
import random
import time
from math import floor

class Music():
    def __init__(self, mode, debug_time_delay):
        self.melody_met = Metro(0.5).play()
        self.bass_met = Metro(2).play()
        self.chord_met = Metro(2).play()
        self.debug_time_delay = debug_time_delay
        self.current_mode_name = mode
        
        # Simple progressions using the primary triads (I, IV, and V) in each mode.
        # The I chord is repeated to help establish the mode and we use open voicings to make
        # the chords more full and less muddy in the low registers. To make an open voicing, we
        # move the middle note of the triad up an octave by adding 12 to the original midi number.
        
        self.mode_primary_triads = {
            "ionian": [['G1', 'B2', 'D2'], ['G1', 'B2', 'D2'], ['C2', 'E3', 'G2'], ['D2', 'F#3', 'A2'], ['E2', 'F#3', 'B2'], ['B3', 'C4', 'D4']],
            "dorian": [['A1', 'C3', 'E2'], ['A1', 'C3', 'E2'], ['D2', 'F#3', 'A2'], ['E2', 'G3', 'B2']],
            "phrygian": [['B1', 'D3', 'F#2'], ['B1', 'D3', 'F#2'], ['E2', 'G3', 'B2'], ['F#2', 'A3', 'C3']],
            "lydian": [['C2', 'E3', 'G2'], ['C2', 'E3', 'G2'], ['F#2', 'A3', 'C3'], ['G2', 'B3', 'D3']],
            "mixolydian": [['D2', 'F#3', 'A2'], ['D2', 'F#3', 'A2'], ['G2', 'B3', 'D3'], ['A2', 'C4', 'E3']],
            "aeolian": [['E1', 'G2', 'B1'], ['E1', 'G2', 'B1'], ['A1', 'C3', 'E2'], ['B1', 'D3', 'F#2']],
            "locrian": [['F#1', 'A2', 'C2'], ['F#1', 'A2', 'C2'], ['B1', 'D3', 'F#2'], ['C2', 'E3', 'G2']],
            "octatonic": [['G1', 'Bb2', 'Db2'], ['G1', 'Bb2', 'Db2'], ['C#2', 'E3', 'G2'], ['D2', 'F3', 'Ab2']]
        }
        
        self.current_triad = 0

        # each note of the motif is represented as an array containing the scale degree and duration in seconds
        # 1 = quarter note, 0.5 = eighth, etc.
        self.motifs = [[[4, 0.25], [5, 0.25], [6, 0.25], [7, 0.5]], 
                       [[4, 0.25], [4, 0.5], [4, 0.25], [2, 1]]]

        self.playing_motif = False
        self.use_motif = 0
        self.motif_num = 0
        self.motif_step = 0

        self.melody_note = 60
        self.harmony_note = 57
        self.harmony_interval = 5
        self.harmonizing = False
        self.bass_note = 28
        
        self.melody_vol = 0.3
        self.harmony_vol = 0.3
        
        self.notes_to_harmonize = 0
        
        self.guitar_sample_speed = 1
        # 1 = forward, -1 = backward
        self.guitar_sample_direction = 1
        
        self.g_guitar_samples = {"dummy": []}
        self.fsharp_guitar_samples = {"dummy": []}
        
        self.g_midi_numbers = [28, 30, 31, 33, 35, 36, 38, 40, 42, 43, 45, 47, 48, 
                             50, 52, 54, 55, 57, 59, 60, 62, 64, 66, 69]
        
        self.fsharp_midi_numbers = [27, 29, 32, 34, 37, 39, 41, 44, 46, 49, 51, 53,
                                   56, 58, 61, 63, 65, 67, 68]
        
        self.octatonic_midi_numbers = [28, 29, 31, 32, 34, 35, 37, 38, 40, 41, 43, 44, 46, 47, 49, 
                                       50, 52, 53, 55, 56, 58, 59, 60, 62, 63, 65, 66, 68, 69]

        self.guitar_mixer = Mixer(time=0.2)
        self.current_guitar_channel = 0
        
        self.reverb_state = False
        
        # Effects signal chain: 
        self.distortion = Disto(self.guitar_mixer[0], drive=0)
        
        self.guitar_delay = Delay(self.distortion, 0.1, 0.7, 5)
        self.delay_selector = Selector(inputs=[self.distortion, self.guitar_delay], mul=[0.5, 0.5], voice=0)
        
        # We don't create a selector object for the reverb so we can directly control the amount 
        # of wet reverb signal while leaving the original signal audible
        self.reverb_fader = Fader()
        self.reverb = STRev(self.delay_selector, revtime=10, mul=self.reverb_fader).out()
        
        # LFO = Low Frequency Oscillator - a signal used to modulate some paramater of the sound like pitch or volume 
        # Modulate is a fancy way of saying change over time
        self.pitch_lfo = Sine(freq=0, mul=1, add=1)
        
        self.detune = False
        self.detune_factor = 0.1

        self.load_guitar_samples()
                             
        self.melody_player = TrigFunc(self.melody_met, self.play_melody)
        # self.countermelody_player = TrigFunc(self.melody_met, self.play_melody)
        self.chord_player = TrigFunc(self.chord_met, self.play_chords)
    
    def load_guitar_samples(self):
        """Loads guitar soundfiles into SfPlayers\n
    Changes to reversed samples when user types 'rt'"""
        # print("load_guitar_samples")
        # print("Glug glug glug...", end="")
        self.melody_met.stop()
        self.chord_met.stop()
        # time.sleep(2) # for debugging purposes
        self.guitar_mixer.setMul(0)
        time.sleep(self.debug_time_delay) # for debugging purposes
        # print(".", end="")
        self.guitar_mixer.clear()
        self.current_guitar_channel = 0
        if self.guitar_sample_direction == 1:
            samples = "guitar_samples"
        else:
            samples = "reversed_guitar_samples"
        
        for m in self.g_midi_numbers:
            # print(f"m: {m}")
            for i in range(0, 3):
                try:
                    # print(f"i: {i}")
                    sample_array = [Adsr(attack=0.01, sustain=1, release=0.1, dur=5, mul=1), SfPlayer(f"soundfiles/{samples}/{m}-{i+1}.aif", 
                                                                      speed=self.pitch_lfo
                                                                      ).stop()]
                    self.g_guitar_samples[f"{m}-{i+1}"] = sample_array
                    self.g_guitar_samples[f"{m}-{i+1}"][1].mul = self.g_guitar_samples[f"{m}-{i+1}"][0]
                    if self.current_guitar_channel < 200:
                        self.guitar_mixer.addInput(self.current_guitar_channel, self.g_guitar_samples[f"{m}-{i+1}"][1])
                        self.guitar_mixer.setAmp(self.current_guitar_channel, 0, 1)
                        self.guitar_mixer.setAmp(self.current_guitar_channel, 1, 1)
                        self.current_guitar_channel += 1
                    # print(f"self.current_guitar_channel g: {self.current_guitar_channel}")
                except Exception as e:
                    # print("g exception: " + str(e))
                    pass
                    
            #print(self.g_guitar_samples)
                    
        for m in self.fsharp_midi_numbers:
            for i in range(0, 3):
                try:
                    # print(f"i: {i}")
                    sample_array = [Adsr(attack=0.01, sustain=1, release=0.1, dur=2), SfPlayer(f"soundfiles/{samples}/{m+1}-{i+1}.aif", 
                                                                           speed=self.pitch_lfo*0.9438)
                                    ]
                    self.fsharp_guitar_samples[f"{m}-{i+1}"] = sample_array
                    self.fsharp_guitar_samples[f"{m}-{i+1}"][1].mul = self.fsharp_guitar_samples[f"{m}-{i+1}"][0]
                    
                    if self.current_guitar_channel < 200:
                        self.guitar_mixer.addInput(self.current_guitar_channel, self.fsharp_guitar_samples[f"{m}-{i+1}"][1])
                        self.guitar_mixer.setAmp(self.current_guitar_channel, 0, 1)
                        self.guitar_mixer.setAmp(self.current_guitar_channel, 1, 1)
                        self.current_guitar_channel += 1
                    # print(f"self.current_guitar_channel fsharp: {self.current_guitar_channel}")
                except Exception as e:
                    #print("f# exception: " + str(e))
                    pass
        
        # Claude suggested silently triggering the samples once like this would get rid of the clicking,
        # but so far it doesn't seem to work
                
        # for key in self.g_guitar_samples.keys():
        #     if key!= "dummy":
        #         self.g_guitar_samples[key][1].setMul(0)
        #         self.g_guitar_samples[key][1].play()
        #         self.g_guitar_samples[key][0].play()
        
        # for key in self.fsharp_guitar_samples.keys():
        #     if key!= "dummy":
        #         self.fsharp_guitar_samples[key][1].setMul(0)
        #         self.fsharp_guitar_samples[key][1].play()
        #         self.fsharp_guitar_samples[key][0].play()
        
        time.sleep(self.debug_time_delay)
        
        # for key in self.g_guitar_samples.keys():
        #     if key!= "dummy":
        #         self.g_guitar_samples[key][1].setMul(1)
        
        # for key in self.fsharp_guitar_samples.keys():
        #     if key!= "dummy":
        #         self.fsharp_guitar_samples[key][1].setMul(1)
        
        self.guitar_mixer.setMul(1)
        time.sleep(self.debug_time_delay) # for debugging purposes
        # print(".")
        self.melody_met.play()
        self.chord_met.play()
        
    # Plays a single note on the guitar
    # The try...except statements here account for the difference in numbers of samples for each pitch.
    # Some notes are sampled at 5 different dynamic levels, while others have only 2.
    #
    # [0] = envelope
    # [1] = sfplayer
    def play_guitar(self, note):
        """
        Plays a single note on the guitar accounting for amount of detune and whether or not the note is the G major scale
        """
        dynamic_level = random.randint(1, 3)
        if note in self.g_midi_numbers:    
            try:
                if self.detune:
                    self.g_guitar_samples[f"{note}-{dynamic_level}"][1].setSpeed(self.pitch_lfo + (random.random() * self.detune_factor))
                else:
                    self.g_guitar_samples[f"{note}-{dynamic_level}"][1].setSpeed(self.pitch_lfo)
                self.g_guitar_samples[f"{note}-{dynamic_level}"][1].play()
                self.g_guitar_samples[f"{note}-{dynamic_level}"][0].play()
            except Exception as e:
                if self.detune:
                    self.g_guitar_samples[f"{note}-{dynamic_level-1}"][1].setSpeed(self.pitch_lfo+(random.random() * self.detune_factor))
                else:
                    self.g_guitar_samples[f"{note}-{dynamic_level-1}"][1].setSpeed(self.pitch_lfo)
                
                self.g_guitar_samples[f"{note}-{dynamic_level-1}"][1].play()
                self.g_guitar_samples[f"{note}-{dynamic_level-1}"][0].play()
        else:
            try:
                if self.detune:
                    self.fsharp_guitar_samples[f"{note}-{dynamic_level}"][1].setSpeed(self.pitch_lfo+(random.random() * self.detune_factor))
                else:
                    self.fsharp_guitar_samples[f"{note}-{dynamic_level}"][1].setSpeed(0.9438 * self.pitch_lfo)
                self.fsharp_guitar_samples[f"{note}-{dynamic_level}"][1].play()
                self.fsharp_guitar_samples[f"{note}-{dynamic_level}"][0].play()
            except Exception as e:
                if self.detune:
                    self.fsharp_guitar_samples[f"{note}-{dynamic_level-1}"][1].setSpeed(0.9438 * self.pitch_lfo+(random.random() * self.detune_factor))
                else:
                    self.fsharp_guitar_samples[f"{note}-{dynamic_level-1}"][1].setSpeed(0.9438 * self.pitch_lfo)    
                self.fsharp_guitar_samples[f"{note}-{dynamic_level-1}"][1].play()
                self.fsharp_guitar_samples[f"{note}-{dynamic_level-1}"][0].play()

    def play_melody(self):
        """
        Generates a melody using randomly chosen notes and rhythms with the occasional inclusion of motifs\n
        Harmonizes melody at randomized intervals for randomized lengths of time
        """
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
        
        if self.use_motif > 0:
            self.playing_motif = True
            
        if self.playing_motif:
            if modify_motif_pitch > 0.75:
                # print(f"old motif pitches: {self.motifs[self.motif_num]}")
                note_to_change = floor(random.random() * 4)
                change_interval = random.choice([-1, 1])
                
                # pitch is the first number in the motif array so we access it with [0]
                self.motifs[self.motif_num][note_to_change][0] = self.motifs[self.motif_num][note_to_change][0] + change_interval
                # print(f"new motif pitches: {self.motifs[self.motif_num]}")
                
            if modify_motif_rhythm > 0.75:
                # print(f"old motif rhythm: {self.motifs[self.motif_num]}")
                note_to_change = floor(random.random() * 4)
                
                # rhythm is the second number in the motif array so we access it with [1]
                # the list comprehension here makes it so that we always change to a new rhythmic value
                # rather than randomly selecting the same one  
                self.motifs[self.motif_num][note_to_change][1] = random.choice([r for r in [0.25, 0.5, 0.75, 1] if r != self.motifs[self.motif_num][note_to_change][1]])
                # print(f"new motif rhythm: {self.motifs[self.motif_num]}")
                
            play_note = 1 # make sure no notes of the motif are replaced with rests
            
            if self.current_mode_name == "octatonic":
                if self.motif_step < len(self.motifs[self.motif_num]) - 1:
                    # print(f"motif {self.motif_num}, self.motif_step {self.motif_step}, motif degree: {self.motifs[self.motif_num][self.motif_step]}, scale_note: {self.current_mode[self.motifs[self.motif_num][self.motif_step][0] - 1]}")
                    
                    self.melody_note = self.octatonic_midi_numbers[8 + self.motifs[self.motif_num][self.motif_step][0]]
                    
                    # if the harmony note is out of range, don't play it
                    try:
                        self.harmony_note = self.octatonic_midi_numbers[8 + self.harmony_interval + self.motifs[self.motif_num][self.motif_step][0]]
                    except Exception as e:
                        print(e)
                    
                    self.melody_met.setTime(self.motifs[self.motif_num][self.motif_step][1])
                    self.motif_step += 1
                else:
                    self.melody_note = self.octatonic_midi_numbers[8 + self.motifs[self.motif_num][self.motif_step][0]]
                    try:
                        self.harmony_note = self.octatonic_midi_numbers[8 + self.harmony_interval + self.motifs[self.motif_num][self.motif_step][0]]
                    except Exception as e:
                        print(e)
                    self.melody_met.setTime(self.motifs[self.motif_num][self.motif_step][1])
                    self.motif_step = 0
                    self.playing_motif = False
            else:
                if self.motif_step < len(self.motifs[self.motif_num]) - 1:
                    # print(f"motif {self.motif_num}, self.motif_step {self.motif_step}, motif degree: {self.motifs[self.motif_num][self.motif_step]}, scale_note: {self.current_mode[self.motifs[self.motif_num][self.motif_step][0] - 1]}")
                    
                    self.melody_note = self.g_midi_numbers[8 + self.motifs[self.motif_num][self.motif_step][0]]
                    
                    # if the harmony note is out of range, don't play it
                    try:
                        self.harmony_note = self.g_midi_numbers[8 + self.harmony_interval + self.motifs[self.motif_num][self.motif_step][0]]
                    except Exception as e:
                        print(e)
                    
                    self.melody_met.setTime(self.motifs[self.motif_num][self.motif_step][1])
                    self.motif_step += 1
                else:
                    self.melody_note = self.g_midi_numbers[8 + self.motifs[self.motif_num][self.motif_step][0]]
                    try:
                        self.harmony_note = self.g_midi_numbers[8 + self.harmony_interval + self.motifs[self.motif_num][self.motif_step][0]]
                    except Exception as e:
                        print(e)
                    self.melody_met.setTime(self.motifs[self.motif_num][self.motif_step][1])
                    self.motif_step = 0
                    self.playing_motif = False   
        else:
            random_degree = random.randint(0, 23)
            if self.current_mode_name == "octatonic":
                self.melody_note = self.octatonic_midi_numbers[random_degree]
                try:
                    self.harmony_note = self.octatonic_midi_numbers[random_degree + self.harmony_interval]
                except Exception as e:
                    print(e)
            else:
                self.melody_note = self.g_midi_numbers[random_degree]
                try:
                    self.harmony_note = self.g_midi_numbers[random_degree + self.harmony_interval]
                except Exception as e:
                    print(e)

        # print(f"notes_to_harmonize: {notes_to_harmonize}")
        if self.notes_to_harmonize == 0:
            harmonize = random.random()
            if harmonize > 0.6:
                self.harmonizing = True
                self.notes_to_harmonize = 3 + random.randint(0, 5)
                self.harmony_interval = random.randint(2, 5)
                # print(f"self.harmony_interval: {self.harmony_interval}")
                # print(f"interval of harmonization: {self.harmony_interval + 1}")
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
        """
        Plays a chord in the progression
        """
        #print(self.mode_primary_triads[self.current_mode_name][self.current_triad])
        # print(len(self.mode_primary_triads[self.current_mode_name]))
        self.play_guitar(self.note_to_midi(self.mode_primary_triads[self.current_mode_name][self.current_triad][0]))
        self.play_guitar(self.note_to_midi(self.mode_primary_triads[self.current_mode_name][self.current_triad][1]))
        self.play_guitar(self.note_to_midi(self.mode_primary_triads[self.current_mode_name][self.current_triad][2]))
        
        if self.current_triad < len(self.mode_primary_triads[self.current_mode_name]) - 1:
            self.current_triad += 1
        else:
            self.current_triad = 0

        #print(f"self.current_triad after: {self.current_triad}")
  
    def toggle_guitar_reverb(self):
        if self.reverb_state:
            self.reverb_fader.stop()
            self.reverb_state = False
        else:
            self.reverb_fader.play()
            self.reverb_state = True
            
    def set_reverb_length(self, time):
        self.reverb.setRevtime(time)
        
    def toggle_guitar_delay(self):
        # print("toggle delay start")
        if self.delay_selector.voice == 0:
            self.delay_selector.voice = 1
        else:
            self.delay_selector.voice = 0
        # print("toggle delay end")

    def change_guitar_delay(self, delay):
        """
        Changes the delay time
        """
        print('called change_guitar_delay')
        self.guitar_delay.setDelay(delay)
        
    def change_mode(self, mode):
        #print("changing mode")
        #print(mode)
        self.current_mode_name = mode
        # self.current_mode = self.modes[mode]
        #print(self.modes[mode])
        
    def reverse_samples(self):
        self.guitar_sample_direction = -1 * self.guitar_sample_direction
        self.load_guitar_samples()
        # print("reverse_samples")
        # if self.guitar_sample_speed == 1:
        #     for m in self.g_midi_numbers:
        #         # print(f"if m: {m}")
        #         for i in range(0, 3):
        #             try:
        #                 # print(f"i: {i}")
        #                 self.guitar_sample_speed = -1
        #                 self.g_guitar_samples[f"{m}-{i+1}"].setSpeed(-1)
        #                 # print(f"self.guitar_channel: {self.guitar_channel}")
        #             except Exception as e:
        #                 # print("exception: " + str(e))
        #                 pass          
        # else:
        #     for m in self.g_midi_numbers:
        #         # print(f"else m: {m}")
        #         for i in range(0, 3):
        #             try:
        #                 # print(f"i: {i}")
        #                 self.guitar_sample_speed = 1
        #                 self.g_guitar_samples[f"{m}-{i+1}"].setSpeed(1)
        #                 # print(f"self.guitar_channel: {self.guitar_channel}")
        #             except Exception as e:
        #                 # print("exception: " + str(e))
        #                 pass
 
    # Converts notes written in pitch/octave format like "C4" to MIDI numbers 0-127
    # Written by Claude 4 Sonnet
    def note_to_midi(self, note):
        # Note name to semitone mapping (C = 0)
        note_values = {
            'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11
        }
        
        # Parse the note string
        note = note.strip()
        
        # Extract note name (first character)
        note_name = note[0]
        if note_name not in note_values:
            raise ValueError(f"Invalid note name: {note_name}")
        
        # Find where the octave number starts
        octave_start = 1
        accidentals = ""
        
        # Extract accidentals (sharps and flats)
        for i in range(1, len(note)):
            if note[i].isdigit() or note[i] == '-':
                octave_start = i
                break
            accidentals += note[i]
        
        # Extract octave number
        try:
            octave = int(note[octave_start:])
        except ValueError:
            raise ValueError(f"Invalid octave number in note: {note}")
        
        # Calculate base MIDI number
        base_midi = note_values[note_name] + (octave + 1) * 12
        
        # Apply accidentals
        accidental_offset = 0
        for char in accidentals:
            if char == '#':
                accidental_offset += 1
            elif char == 'b' or char == 'B':  # Flat
                accidental_offset -= 1
            else:
                raise ValueError(f"Invalid accidental: {char}")
        
        midi_number = base_midi + accidental_offset
        
        # Ensure MIDI number is in valid range (0-127)
        if midi_number < 0 or midi_number > 127:
            raise ValueError(f"MIDI number {midi_number} out of range (0-127)")
        
        return midi_number

    def stop(self):
        self.melody_met.stop()
        self.chord_met.stop()
        self.bass_met.stop()