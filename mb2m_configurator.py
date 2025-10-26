#Configurator
import sys, tomllib, tomli_w
from rtmidi2 import MidiIn, MidiOut, get_in_ports, get_out_ports
import json, time
from simple_term_menu import TerminalMenu
import os
from mb2m_lib import init_midi_in, init_midi_out, read_config, write_config, read_map, write_map, midi_to_abc, midi_list_to_abc, init_midi_aux_in

#initializes midi to config
def init_midi():
    global MIDIINPORT, MIDIOUTPORT, MIDIAUXINPORT
    print("*MIDI Port Initialization*")
    MIDIINPORT = init_midi_in()
    MIDIOUTPORT = init_midi_out()
    MIDIAUXINPORT = init_midi_aux_in()

#flushes midi to prevent program errors
def flush_midi_input(port):
    """Discard all pending MIDI messages in the input buffer."""
    while True:
        msg = port.get_message()
        if msg is None:
            break

def startup_check():
    config = read_config("config.toml")
    if len(config["MIDI"]["midi_input_port"]) < 1:
        #print("MIDI in port not configured")
        set_MIDI_input()
    if len(config["MIDI"]["midi_output_port"]) < 1:
        set_MIDI_output()
    if len(config["MIDI"]["midi_aux_in_port"]) < 1:
        set_MIDI_aux_input()

def get_midi_note_trigger(port):
    flush_midi_input(port)
    #midiin = MidiIn()
    #midiin.open_port(0) 
    print("Enter a midi byte2 note from your foot controller to be used as a trigger: ")
    
    msg = port.get_message()
    
    while msg is None:
        msg = port.get_message()
        if msg:
            for m in msg:
                #print(msg)
                None
    #port.close_port()
    
    return msg[1]

def get_chord(port, timeout=0.5):
    flush_midi_input(port)
    #midiin = MidiIn()
    #midiin.open_port(0) 
    print(f"Enter a chord and hold for {timeout} seconds from your aux controller")
    
    notes = set()
    last = time.time()
    
    while True:
        msg = port.get_message()
        
        if msg:
            
            # msg might be just a list like [status, note, velocity]
            if isinstance(msg, tuple):
                msg = msg[0]  # use only the MIDI bytes

            status, note, vel = msg

            if status & 0xF0 == 0x90 and vel > 0:   # Note On
                notes.add(note)
                last = time.time()
            elif status & 0xF0 in (0x80, 0x90) and vel == 0:  # Note Off
                notes.discard(note)

        if notes and time.time() - last > timeout:
            break

    
    return sorted(notes)


def add_mapping(inport, auxport):
    os.system('cls' if os.name == 'nt' else 'clear')
    #print(str(get_midi_note_trigger()))
    #print(get_chord())
    while True:

        trigger = get_midi_note_trigger(inport)
        chord = get_chord(auxport)
        print(f"Trigger Note: {trigger} or {midi_to_abc(trigger)}\nChord: {chord} or {midi_list_to_abc(chord)}")
        choice = input("Confirm mapping (y/n)...\n")

        if choice == "y":
            map = read_map("midi_map.json") #Read map
            map["map"].update({str(trigger):chord}) #Update with data
            write_map("midi_map.json", map) #write json
            print("Map Updated.")
            return
        else:
            return
    return

def remove_mapping():
    os.system('cls' if os.name == 'nt' else 'clear')
    map = read_map("midi_map.json")
    
    print("\n*current mappings*")
    view_map()
    print("\n")
    choice = input("Enter 0x90 value input to be removed...")
    
    if choice in map["map"]:
        mapping = map["map"][choice]
        removed_value = map["map"].pop(str(choice))
        print(f"removed 0x90 {choice} with mapping {mapping}")
    
        with open("midi_map.json", 'w') as file:
            json.dump(map, file, indent=2)
        return
    else:
        print(f"ERROR: mapping with input 0x90 value: {choice} does not exist in the map")
        input("Press enter to continue\n")

#Set configs midi in
def set_MIDI_input():
    os.system('cls' if os.name == 'nt' else 'clear')
    config = read_config('config.toml')
    ports = get_in_ports()

    menu = TerminalMenu(ports, title="Select a MIDI Input Port")
    choice_index = menu.show()

    if choice_index is not None:
        choice = ports[choice_index]
    
    config['MIDI']['midi_input_port'] = choice
    write_config('config.toml', config)
    init_midi_in()
    print(f"CONFIG: MIDI input port set to {choice}")

#set configs midi out
def set_MIDI_output():
    os.system('cls' if os.name == 'nt' else 'clear')
    config = read_config('config.toml')
    ports = get_out_ports()

    menu = TerminalMenu(ports, title="Select a MIDI Output Port")
    choice_index = menu.show()

    if choice_index is not None:
        choice = ports[choice_index]
    
    config['MIDI']['midi_output_port'] = choice
    write_config('config.toml', config)
    init_midi_out()
    print(f"CONFIG: MIDI out port set to {choice}")

#set configs aux midi in
def set_MIDI_aux_input():
    os.system('cls' if os.name == 'nt' else 'clear')
    config = read_config('config.toml')
    ports = get_in_ports()

    menu = TerminalMenu(ports, title="Select a MIDI Aux Input Port")
    choice_index = menu.show()

    if choice_index is not None:
        choice = ports[choice_index]
    
    config['MIDI']['midi_aux_in_port'] = choice
    write_config('config.toml', config)
    init_midi_aux_in()
    print(f"CONFIG: MIDI aux in port set to {choice}")

#print the map file
def view_map():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Midi Mappings")
    map = read_map("midi_map.json")
    text = "Trigger : Chord\n"
    for i in map["map"]:
        text += str(midi_to_abc(int(i))) + f" or {i}" + ": "
        for j in map["map"][i]:
            text += str(midi_to_abc(int(j))) + " "
        print(text)
        text = ""
    

#User menu switch
def user_switch(num):
    match num:
        case 1:
            add_mapping(MIDIINPORT, MIDIAUXINPORT)
        case 2:
            remove_mapping()
        case 3:
            set_MIDI_input()
        case 4:
            set_MIDI_output()
        case 5:
            view_map()
        case 6:
            set_MIDI_aux_input()
        case 7:
            os.system('cls' if os.name == 'nt' else 'clear')
            sys.exit()


home_menu = ["Add mapping", "Remove Mapping", "Set MIDI In Port", "Set MIDI Out Port", "View Map", "Set MIDI Aux In Port","Exit"]
startup = "\n*************************************" \
          "\nMIDI byte2 Mutator Configurator" \
          "\nBrandon Pettenati" \
          "" \
          "\n*************************************\n"

def main():
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(startup)
    startup_check()
    init_midi()
    


    while True:
        
        
        menu = TerminalMenu(home_menu, title="\n-----NTC Configurator. Choose an option-----\n")
        choice_index = menu.show()

        if choice_index is not None:
            
            user_switch(choice_index+1)
        #choice = input("Make a numerical selection...\n")
        #user_switch(int(choice))
main()