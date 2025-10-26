# Mb2M

Also known as the <em>MIDI byte2 Mutator</em> is an inline MIDI mutator allowing for note on/off byte 2 messages to be intercepted and output a collection of notes as defined by the user. The idea of this program is to allow the user to connect a MIDI triggering device such as a footswitch and then be able to have a chord be outputed based on predefined user mappings.Thus allowing the user to play a synth or VST accompionment while performing on another instrument. 

### Program Contents
The program consists of two smaller individual programs: 
    the real-time note to chord mutator (mb2m.py) and a configurator program (mb2m_configurator.py)

Included as well is the required user configurable file:
    the file containing the MIDI mappings (midi_map.json) and a config file to store the users MIDI in and out port (config.toml)

There is also a mb2m_lib.py that holds necessay code for both programs.

### Dependencies
1. python3
2. simple_term_menu
3. rtmidi2
4. tomllib
5. tomli_w

### Implementation
mb2m.py is intended to ran as a headless MIDI server within an OS. The program is build almost entirely with python allowing it to be cross-platform and should run on Mac, Windows and Linux. However only MacOS has been tested at this point. The program can be run on a normal desktop or it can conversely be used on a Raspberry Pi or another SBC inconjunction with a MIDI interface with an in and out port to act as a pseudo hardware device. In the programs current state the latter option would be cumbersome as the SBC would need to be interfaced via keyboard and monitor, SSH, or some other form of interfacing.

## Program Operation
Both the config and midi_map files are required for both the operation of the main mb2m server as well as the configurator. 

The configurator consists of 6 subsections:
1. Add Mapping - used to map a MIDI input note value to multiple output note values
2. Remove Mapping - used to delete a mapping
3. Set MIDI Input - used to find in port devices within your system and set it
4. Set MIDI output - used to find out port devices within your system and set it
5. View Map - used to view a nicely formatted version of you mappings with note names


#### Add Mapping
The add mapping function consists of a MIDI learn to make adding mappings easier. The program will prompt you for an input trigger. You can play whatever you want your trigger note to be from your foot controller or whatever MIDI controller you are using. It will then promt you to play and hold your desired output chord for a second. After viewing and confirming you mapping it will be added to the map. Conversely you can also manually edit the note values within the midi_map.json.

#### MIDI Mutation
It is important to note that in the current state only byte2 of the MIDI message will be mutated. The status, channel and velocity (byte 1 and 3) will be unaltered and passed through to the output. Hence the name MIDI byte2 Mutator. The program will also only detect NOTE ON and OFFS.

A sample mapping in hex could look like:
```text
            Input
      b1           b2       b3
0x    91           3C       40
      \______________________/
                      |               Output
                      |             b1  b2  b3
                      |------------ 91  3C  40
                      |------------ 91  40  40
                      |------------ 91  43  40
```
And in English:
```text
            Input
  b1             b2         b3
  NOTEON Ch1     C4     vel 64 
  \__________________________/
                      |                        Output
                      |              b1             b2         b3
                      |------------- NOTEON Ch1     C4     vel 64 
                      |------------- NOTEON Ch1     E4     vel 64 
                      |------------- NOTEON Ch1     G4     vel 64 
```

Only the note value or byte2 will change.

