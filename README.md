# Castle of Sound

This choose-your-own-adventure command line game includes a soundtrack that the user can manipulate through moving to different parts of the castle and acquiring various objects. (The latter is a work in progress). The soundtrack has two parts. The first is acoustic guitar music that is generated using algorithms with random components. The second element is recordings of various ambient noises like footsteps, birds, and background conversation. Run it from the command line with `python3 main.py`.

Download the soundfiles needed from [here](https://drive.google.com/drive/folders/1GT2uNe9idCnJlRWD0WYllIviSZOjfrqh?usp=sharing) and place in the `soundfiles` directory. Soundfiles are relatively large even when using the most space-efficient .mp3 format. Git's way of storing and transmitting them along with the rest of the repo is way less efficient than simply uploading to a cloud service.

The `soundfiles/guitar_samples` folder contains guitar samples from the Logic Pro acoustic guitar instrument which is exclusively notes from G major. On the piano, this is all the white keys except for F# which replaces F natural. The soundfiles have labels of the form MidiNumber-Velocity, where the velocity is a number between 1 and 4. Interestingly, some notes are sampled at 4 different dynamics while other have only 2.

# Why a command line game?

Command line games are a great educational tool because they can be entertaining without the overhead of manipulating graphics. In my experience, getting user interfaces to look right on screen and designing them well is one of the most tedious parts of coding. The focus on music helps make it so that changing just a few parameters in the code can result in wildly different sounds and it's quite easy to create new features that allow a new kind of control. This helps teach any ability to memorize short commands that are a good primer for becoming a command line wizard in the future.

Playing with a command line program like this is also a fun way to connect to our past.In the early days of computers, people didn't have the same user interfaces that we have today. Instead of a brightly lit multicolored screen, early consumer computers in the 1960s mainly consisted of typing commands directly into a textbox called the Command Line Interface. Previously computers had to be programmed with punch cards, a practice that started in 1890. For a thorough history of computing, read more [here](https://plato.stanford.edu/entries/computing-history/) 

This project uses the `pyo` Python audio module: https://github.com/belangeo/pyo
Listen to music created with pyo here: https://radiopyo.acaia.ca/

TODO:
 - Make each soundtrack more different musically
 - Instruments you can play from the command line
 - Potions/spells/powerups/knowledge - echoes, reversal in time, high pass, low pass, band pass, 7th chords, extensions, atonality, micropolyphony
 - Create commands for user to use similar to shell commands that activate certain instruments or turn on certain effects
 - Possible effects
    - Delay
    - High and Low Pass filters
    - Distortion
    - Pitch bend
    - Chromaticism
    - Reverb
    - Reversed samples

Backlog:
 - Counterpoint
 - Imitation
 - Control interval of harmonization



