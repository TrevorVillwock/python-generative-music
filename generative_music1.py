from pyo import *

s = Server().boot()
s.start()

melody_met = Metro(0.5).play()
bass_met = Metro(2).play()

scale = [0, 2, 3, 5, 7, 9, 10, 12]

# using scale degrees
motifs = [[1, 3, 2, 4], [5, 5, 5, 7, 6]]
playing_motif = False
motif_step = 0

melody_env = Adsr(0.1, dur=0.25)
bass_env = Adsr(0.1, release=1, dur=2)

# Square waveform generator
melody_wav = SquareTable(5)
bass_wav = SquareTable(5)

melody_synth = Osc(table=melody_wav, freq=[220, 220], mul=melody_env)

bass_synth = Osc(table=bass_wav, freq=[midiToHz(36), midiToHz(36)], mul=bass_env).out()

melody_reverb = Freeverb(melody_synth, 2).out()

def play_melody():
    global playing_motif, motifs, motif_step
    # print("play_melody")
    play_note = random.random() * 3
    use_motif = random.random() * 4
    
    motif_num = round(random.random())
    change_rhythm = random.random() * 4
    
    if change_rhythm > 2:
        melody_met.setTime(random.choice([0.25, 0.5, 0.75, 1]))
    
    if use_motif > 3:
        playing_motif = True
        
    if playing_motif:
        print("playing motif")
        play_note = 3 # make sure no notes of the motif are replaced with rests
        if motif_step < len(motifs[motif_num]) - 1:
            print(f"motif_num: {motif_num}")
            print(f"motif_step: {motif_step}")
            print(f"motifs[motif_num][motif_step]: {motifs[motif_num][motif_step]}")
            melody_synth.setFreq(midiToHz(60 + scale[motifs[motif_num][motif_step]]))
            motif_step += 1
        else:
            motif_step = 0
            playing_motif = False
    else:
        melody_synth.setFreq(midiToHz(60 + scale[random.randint(0, 7)]))
        
    if play_note > 1:
        melody_env.play()
        print("playing melody")

def play_bass():
    # print("play_bass")
    change_note = random.random() * 3
    if change_note > 0:
        # print("playing bass")
        bass_synth.setFreq(midiToHz(36 + scale[random.randint(0, 7)]))
    bass_env.play()

melody_player = TrigFunc(melody_met, play_melody)
bass_player = TrigFunc(bass_met, play_bass)

s.gui(locals)