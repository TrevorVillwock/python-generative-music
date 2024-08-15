from pyo import Metro, SfPlayer, Mixer, TrigFunc, Server
import random
from math import floor

s = Server().boot()
s.start()

guitar_samples = {}
midi_numbers = [28, 30, 31, 33, 35, 36, 38, 40, 42, 43, 45, 47, 48, 
                        50, 52, 54, 55, 57, 59, 60, 62, 64, 66, 69]

guitar_mixer = Mixer(chnls=100).out()

# this will be incremented every time we add a guitar sample to the mixer to provide the channel number 
guitar_channel = 0

guitar_test_sample = SfPlayer(f"soundfiles/guitar_samples/28-1.aif")

# guitar_mixer.addInput(guitar_channel, guitar_test_sample)
# guitar_mixer.setAmp(0, 0, 0.5)

# for m in midi_numbers:
#     # We make the first element of the array None so that the number of the guitar sample
#     # (i.e. the 1 in 28-1) aligns with its index in the list
#     guitar_samples[m] = []
#     guitar_samples[m].append(None)
#     print(f"m: {m}")
#     for i in range (1, 6):
#         print(f"i: {i}")
#         try:
#             # the array here makes it so that the mono guitar sample will play in stereo;
#             # two elements are inputs for the left and right channels
#             # self.guitar_samples[m].append(SfPlayer([f"soundfiles/guitar_samples/{m}-{i}.aif", f"soundfiles/guitar_samples/{m}-{i}.aif"]))
#             guitar_samples[m].append(SfPlayer(f"soundfiles/guitar_samples/{m}-{i}.aif"))
#             # self.guitar_mixer.addInput(self.guitar_channel, self.guitar_samples[m][i])
#             guitar_mixer.addInput(guitar_channel, guitar_samples[m][i])
#             guitar_mixer.setAmp(i, 0, 0.1)
#             print(f"self.guitar_channel: {guitar_channel}")
#             guitar_channel += 1
#         except Exception as e:
#             guitar_samples[m].append(None)
#             # We do this because different notes have different numbers of samples; some are sampled
#             # at 5 dynamic levels while others have only 2 or 3. 
#             # Uncomment the line below to see the exception message.
            
#             print("exception: " + str(e))

for m in midi_numbers:
    # We make the first element of the array None so that the number of the guitar sample
    # (i.e. the 1 in 28-1) aligns with its index in the list
    guitar_samples[m] = SfPlayer(f"soundfiles/guitar_samples/{m}-1.aif").stop()
    # self.guitar_mixer.addInput(self.guitar_channel, self.guitar_samples[m][i])
    guitar_mixer.addInput(guitar_channel, guitar_samples[m])
    guitar_mixer.setAmp(guitar_channel, 0, 0.1)
    print(f"self.guitar_channel: {guitar_channel}")
    guitar_channel += 1

print(guitar_mixer.getChannels())
print(guitar_mixer.getKeys())

def play_guitar():
    # guitar_test_sample.play()
    guitar_samples[random.choice([28, 30, 31, 33, 35, 36, 38, 40, 42, 43, 45, 47, 48, 
                        50, 52, 54, 55, 57, 59, 60, 62, 64, 66, 69])].play()

guitar_mixer.setMul(0.1)
guitar_met = Metro(1).play()
guitar_player = TrigFunc(guitar_met, play_guitar)

s.gui(locals)