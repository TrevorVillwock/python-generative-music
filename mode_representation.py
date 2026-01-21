# This section of code isn't currently being used, but its representation of each mode as half
# steps above the tonic may still prove useful.
# 
# A "mode" in music theory is a version of a scale that starts on a different note than the 
# conventional one but retains the same collection and order of notes.
# Sometimes more complicated definitions are given, but that's the most simple and practical one.
# The numbers in these arrays represent the number of half steps above the first note of the mode.
# The first mode Ionian is the same as the major scale.
#
# self.modes = {"ionian": [0, 2, 4, 5, 7, 9, 11, 12, 
#                          14, 16, 17, 19, 21, 23, 24],
#               "dorian": [0, 2, 3, 5, 7, 9, 10, 12, 
#                          14, 15, 17, 19, 21, 22, 24],
#               "phrygian": [0, 1, 3, 5, 7, 8, 10, 12, 
#                            13, 15, 17, 19, 20, 22, 24],
#               "lydian": [0, 2, 4, 6, 7, 9, 11, 12, 
#                          14, 16, 18, 19, 21, 23, 24],
#               "mixolydian": [0, 2, 4, 5, 7, 9, 11, 12, 
#                              14, 16, 17, 19, 21, 22, 24],
#               "aeolian": [0, 2, 3, 5, 7, 8, 10, 12, 
#                           14, 15, 17, 19, 20, 22, 24],
#               "locrian": [0, 1, 3, 5, 7, 8, 10, 12, 
#                           13, 15, 17, 19, 20, 22, 24],
#               "octatonic": [0, 1, 3, 4, 6, 7, 9, 10, 12, 
#                             13, 15, 16, 18, 19, 21, 22, 24],
#               "whole tone": [0, 2, 4, 6, 8, 10, 12, 14, 16,
#                              18, 20, 22, 24]
# }