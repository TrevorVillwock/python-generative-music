"""
    TODO
    Add rhythm to motifs
    Motivic development
    Imitation
    Control interval of harmonization
    Counterpoint
    Make into class
    Improve timbre
    Add soundfile playback - footsteps, dripping, birds, wind, conversation
"""

from pyo import *

s = Server().boot()
s.start()

melody_met = Metro(0.5).play()
bass_met = Metro(2).play()

melody_env = Adsr(0.1, dur=0.25)

current_articulation = 0

# number of half steps above tonic
# tonic = first note of the scale
# dorian mode is shown here
dorian = [0, 2, 3, 5, 7, 9, 10, 12, 
          14, 15, 17, 19, 21, 22]

lydian = [0, 2, 4, 6, 7, 9, 11, 12, 14, 16, 18, 19, 21, 23, 24]

scale = dorian

# amplitude (volume) envelopes
# these control how the sounds start and stop
# Attack Decay Sustain Release
# Attack - how long the sound takes to start (seconds)
# Decay - how long the sound takes to reach sustain volume from max (seconds)
# Sustain - volume level when note is held (volume from 0.0-1.0)
# Release - how long the note takes to fade away
bass_env = Adsr(0.1, release=1, dur=2)

# using scale degrees
motifs = [[2, 5, 4, 3], [1, 5, 3, 7]]

# [1, 3, 2, 4], [5, 5, 5, 7, 6], [1, 2, 6, 4]
playing_motif = False
use_motif = 0
motif_num = 0
motif_step = 0

# Square waveform generator using first 5 odd harmonics
melody_wav = SquareTable(5)
bass_wav = SquareTable(5)

melody_synth = Osc(table=melody_wav, freq=[midiToHz(60), midiToHz(60)], mul=melody_env)
harmonizing_synth = Osc(table=melody_wav, freq=[midiToHz(60), midiToHz(60)], mul=melody_env)
notes_to_harmonize = 0
bass_synth = Osc(table=bass_wav, freq=[midiToHz(36), midiToHz(36)], mul=bass_env)

melody_reverb = Freeverb(melody_synth, 2)
harmony_reverb = Freeverb(harmonizing_synth, 2)

# if not currently harmonizing, get random value for harmonization
# randomly determine length of harmonization (3 notes minimum), set notes to harmonize
# play next note with harmony, decrement notes_to_harmonize
# once notes_to_harmonize reaches 0, get random value for harmonization

def play_melody():
    global playing_motif, motifs, motif_step, motif_num, use_motif, notes_to_harmonize
    # print("play_melody")
    play_note = random.random()
    change_rhythm = random.random()
    new_rhythm = random.choice([0.25, 0.5, 0.75, 1])

    # print(f"notes_to_harmonize: {notes_to_harmonize}")
    if notes_to_harmonize == 0:
        harmonize = random.random()
        if harmonize > 0.7:
            notes_to_harmonize = 3 + random.randint(0, 5)
    
    if change_rhythm > 0.5:
        melody_met.setTime(new_rhythm)
    
    # 0 = staccato, 1 = legato
    current_articulation = round(random.random())
    if current_articulation == 1:
        # if legato, make duration of envelope same as note length
        melody_env.setDur(new_rhythm)
    else:
        melody_env.setDur(0.25)
        
    if notes_to_harmonize != 0:
        harmonizing_synth.setMul(melody_env)
        notes_to_harmonize -= 1
    else:
        harmonizing_synth.setMul(0)
    
    if not playing_motif:
        use_motif = random.random()
        motif_num = round(random.random())
    
    if use_motif > 0.4:
        playing_motif = True
        
    if playing_motif:
        play_note = 1 # make sure no notes of the motif are replaced with rests
        if motif_step < len(motifs[motif_num]):
            # scale[motifs[motif_num][motif_step]] gives the number of half steps above middle C
            print(f"motif {motif_num}, motif_step {motif_step}, motif degree: {motifs[motif_num][motif_step]}, scale_note: {scale[motifs[motif_num][motif_step] - 1]}")
            melody_synth.setFreq(midiToHz(60 + scale[motifs[motif_num][motif_step] - 1]))
            
            harmonizing_synth.setFreq(midiToHz(60 + scale[(motifs[motif_num][motif_step] + 1) % 13]))
            
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

            # harmonizing_synth.setFreq(5/4 * midiToHz(60 + scale[motifs[motif_num][motif_step]]))
            
            motif_step += 1
        else:
            motif_step = 0
            playing_motif = False
    else:
        random_degree = random.randint(0, 7)
        melody_synth.setFreq(midiToHz(60 + scale[random_degree]))
        harmonizing_synth.setFreq(midiToHz(60 + scale[(random_degree + 2) % 13]))
        # harmonizing_synth.setFreq(5/4 * midiToHz(60 + scale[random_degree]))
      
    if play_note > 0.3:
        melody_env.play()
        # print("playing melody")

def play_bass():
    # print("play_bass")
    change_note = random.random()
    if change_note > 0.3:
        # print("playing bass")
        bass_synth.setFreq(midiToHz(36 + scale[random.randint(0, 7)]))
    bass_env.play()

melody_player = TrigFunc(melody_met, play_melody)
# bass_player = TrigFunc(bass_met, play_bass)

mixer = Mixer(chnls=4).out()

mixer.addInput(0, melody_reverb)
mixer.addInput(1, harmony_reverb)
mixer.addInput(2, bass_synth)

mixer.setAmp(0, 0, 0.1)
mixer.setAmp(1, 0, 0.1)
mixer.setAmp(2, 0, 0.1)

s.gui(locals)