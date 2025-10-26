from rtmidi2 import MidiIn, NOTEON, CC, splitchannel, NOTEOFF, MidiOut 
import time, os, sys

from mb2m_lib import init_midi_in, init_midi_out, read_map, write_map, text_map
from simple_term_menu import TerminalMenu
import tty, termios, select


midi_log = []

def getch():
    
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)            # raw mode
        ch = sys.stdin.read(1)    # read one character
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def reload_config():
    global MIDIINPORT, MIDIOUTPORT
    MIDIINPORT = init_midi_in()
    MIDIOUTPORT = init_midi_out()

def update_midi_log(log, data):
    midi_log.append(data)
    menu = TerminalMenu(midi_log, title="MIDI LOG")
    choice_index = menu.show()

def callback(msg: list, timestamp: float):
    
    global channel, flag
    
    """if len(msg) < 3 or msg[0] >= 0xF0:
        return"""
    # msg is a list of 1-byte strings
    # timestamp is a float with the time elapsed since last midi event
    msgtype, channel = splitchannel(msg[0])

    
    
    if msgtype == NOTEON:
        note, velocity = msg[1], msg[2]
        if velocity > 0:
            if note in chord_map["map"]:
                for n in chord_map["map"][note]:
                    print(f"Note ON: channel={channel}, note={n}, velocity={msg[2]}")
                    MIDIOUTPORT.send_noteon(channel, n, msg[2])
                    #midi_log.append(f"Note ON: channel={channel}, note={n}, velocity={msg[2]}")
                    
        else:
            if note in chord_map["map"]:
                for n in chord_map["map"][note]:
                    print(f"Note OFF: channel={channel}, note={n}, velocity={0}")
                    MIDIOUTPORT.send_noteon(channel, n, 0)
                    #midi_log.append(f"Note OFF: channel={channel}, note={n}, velocity={0}")
        

    elif msgtype == NOTEOFF:
        note, velocity = msg[1], msg[2]
        if note in chord_map["map"]:
            for n in chord_map["map"][note]:
                print(f"Note OFF: channel={channel}, note={n}, velocity={0}")
                #midi_log.append(f"Note OFF: channel={channel}, note={n}, velocity={0}")
                MIDIOUTPORT.send_noteon(channel, n, 0)
                
        
        
    """elif msgtype == CC:
        cc, value = msg[1], msg[2]
        print(f"Control Change: channel={channel}, cc={cc}, value={value}")
"""



startup = "\n*************************************" \
          "\nMIDI byte2 Mutator" \
          "\nBrandon Pettenati" \
          "" \
          "\n*************************************\n"
os.system('cls' if os.name == 'nt' else 'clear')
print(startup)
print("*MIDI Inititialiatzion*")
MIDIINPORT = init_midi_in()
MIDIOUTPORT = init_midi_out()
print()
print("Press q to exit\n")
print("Press c reload MIDI config\n")
print("Press m reload MIDI map\n")

def load_map(file):
    map = read_map(file)
    map["map"] = {int(k): v for k, v in map["map"].items()}
    return map
chord_map = load_map("midi_map.json")
print(text_map()) 
MIDIINPORT.callback = callback


try:
    # Keep the script alive so the callback can run
    while True:
        time.sleep(0.1)
        
    
        """key = getch()
        if key == 'q':
            sys.exit() 
        if key == 'c':
            reload_config()"""
        
except KeyboardInterrupt:
    print("\nStopping MIDI listener...")


# The callback can be cancelled by setting it to None
MIDIINPORT.callback = None

# When you are done, close the port
MIDIINPORT.close_port()
MIDIINPORT.close_port()