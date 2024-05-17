from pyo import *

s = Server().boot()
s.start()

melody_met = Metro(0.5).play()
bass_met = Metro(2).play()

# number of half steps above tonic
# tonic = first note of the scale
# dorian mode is shown here
scale = [0, 2, 3, 5, 7, 9, 10, 12]

# amplitude (volume) envelopes
# these control how the sounds start and stop
# Attack Decay Sustain Release
# Attack - how long the sound takes to start (seconds)
# Decay - how long the sound takes to reach sustain volume from max (seconds)
# Sustain - volume level when note is held (volume from 0.0-1.0)
# Release - how long the note takes to fade away
melody_env = Adsr(0.1, dur=0.25)
bass_env = Adsr(0.1, release=1, dur=2)

# Square waveform generator
melody_wav = SquareTable(5)
bass_wav = SquareTable(5)

melody_synth = Osc(table=melody_wav, freq=[220, 220], mul=melody_env)

bass_synth = Osc(table=bass_wav, freq=[midiToHz(36), midiToHz(36)], mul=bass_env).out()

melody_reverb = Freeverb(melody_synth, 2).out()

def play_melody():
    print("play_melody")
    # random.random() returns value between 0 and 1
    play_note = random.random() * 3
    change_rhythm = random.random() * 4
    melody_synth.setFreq(midiToHz(60 + scale[random.randint(0, 7)]))
    
    if change_rhythm > 2:
        melody_met.setTime(random.choice([0.25, 0.5, 0.75, 1]))
    
    if play_note > 2:
        melody_env.play()
        print("playing melody")

def play_bass():
    print("play_bass")
    change_note = random.random() * 3
    if change_note > 0:
        print("playing bass")
        bass_synth.setFreq(midiToHz(36 + scale[random.randint(0, 7)]))
    bass_env.play()

melody_player = TrigFunc(melody_met, play_melody)
bass_player = TrigFunc(bass_met, play_bass)

s.gui(locals)