"""
    TODO
    Melody harmonization
    Articulation
    Add rhythm to motifs
    Motivic development
    Imitation
    Interval control
    Make into class
"""

from pyo import *

s = Server().boot()
s.start()

melody_met = Metro(0.5).play()
bass_met = Metro(2).play()

# 0 = staccato, 1 = legato
# articulations = [Adsr(0.1, dur=0.25), Adsr(attack=0.1, dur=0.25)]
melody_env = Adsr(0.1, dur=0.25)

current_articulation = 0

# print(articulations["staccato"])

# number of half steps above tonic
# tonic = first note of the scale
# dorian mode is shown here
scale = [0, 2, 3, 5, 7, 9, 10, 12, 
         14, 15, 17, 19, 21, 22]

# amplitude (volume) envelopes
# these control how the sounds start and stop
# Attack Decay Sustain Release
# Attack - how long the sound takes to start (seconds)
# Decay - how long the sound takes to reach sustain volume from max (seconds)
# Sustain - volume level when note is held (volume from 0.0-1.0)
# Release - how long the note takes to fade away
bass_env = Adsr(0.1, release=1, dur=2)

# using scale degrees
motifs = [[1, 3, 2, 4], [5, 5, 5, 7, 6]]
playing_motif = False
use_motif = 0
motif_num = 0
motif_step = 0

# Square waveform generator using first 5 odd harmonics
melody_wav = SquareTable(5)
bass_wav = SquareTable(5)

melody_synth = Osc(table=melody_wav, freq=[midiToHz(60), midiToHz(60)], mul=melody_env)
harmonizing_synth = Osc(table=melody_wav, freq=[midiToHz(60), midiToHz(60)], mul=melody_env)
notes_to_harmonize = 3
bass_synth = Osc(table=bass_wav, freq=[midiToHz(36), midiToHz(36)], mul=bass_env).out()

melody_reverb = Freeverb(melody_synth, 2).out()
harmony_reverb = Freeverb(harmonizing_synth, 2).out()

def play_melody():
    global playing_motif, motifs, motif_step, motif_num, use_motif
    # print("play_melody")
    play_note = random.random()
    change_rhythm = random.random()
    new_rhythm = random.choice([0.25, 0.5, 0.75, 1])
    harmonize = random.random()
    
    if change_rhythm > 0.5:
        melody_met.setTime(new_rhythm)
    
    # 0 = staccato, 1 = legato
    current_articulation = round(random.random())
    if current_articulation == 1:
        # if legato, make duration of envelope same as note length
        melody_env.setDur(new_rhythm)
    else:
        melody_env.setDur(0.25)
  
    # melody_synth.setMul(articulations[current_articulation])
    # harmonizing_synth.setMul(articulations[current_articulation]) 
    # print(f"current_articulation: {current_articulation}")
    
    if not playing_motif:
        use_motif = random.random()
        motif_num = round(random.random())
    
    if use_motif > 0.6:
        playing_motif = True
        
    if playing_motif:
        # print("playing motif")
        play_note = 1 # make sure no notes of the motif are replaced with rests
        if motif_step < len(motifs[motif_num]):
            # print(f"motif_num: {motif_num}")
            # print(f"motif_step: {motif_step}")
            # print(f"motifs[motif_num][motif_step]: {motifs[motif_num][motif_step]}")
            melody_synth.setFreq(midiToHz(60 + scale[motifs[motif_num][motif_step]]))
            # harmonizing_synth.setFreq(5/4 * midiToHz(60 + scale[motifs[motif_num][motif_step]]))
            harmonizing_synth.setFreq(midiToHz(60 + scale[(motifs[motif_num][motif_step] + 2) % 13]))
            motif_step += 1
        else:
            motif_step = 0
            playing_motif = False
    else:
        random_degree = random.randint(0, 7)
        melody_synth.setFreq(midiToHz(60 + scale[random_degree]))
        harmonizing_synth.setFreq(midiToHz(60 + scale[(random_degree + 2) % 13]))
        # harmonizing_synth.setFreq(5/4 * midiToHz(60 + scale[random_degree]))
    
    if harmonize > 0.3 or notes_to_harmonize != 0:
        harmonizing_synth.setMul(melody_env)
        notes_to_harmonize = 3 + random.randint(0, 5)

    else:
        harmonizing_synth.setMul(0)
      
    if play_note > 0.3:
        melody_env.play()
        print("playing melody")

def play_bass():
    # print("play_bass")
    change_note = random.random()
    if change_note > 0.3:
        # print("playing bass")
        bass_synth.setFreq(midiToHz(36 + scale[random.randint(0, 7)]))
    bass_env.play()

melody_player = TrigFunc(melody_met, play_melody)
bass_player = TrigFunc(bass_met, play_bass)

s.gui(locals)