from rtmidi2 import MidiIn, NOTEON, CC, splitchannel, NOTEOFF, MidiOut, get_in_ports, get_out_ports
import tomllib, tomli_w
import json

def init_midi_in():
    config = read_config('config.toml')
    ports = get_in_ports()
    target_name = config["MIDI"]['midi_input_port']
    for i, name in enumerate(ports):
        if target_name in name:
            inport = MidiIn()
            inport.open_port(i)
            print(f"IN: Opened in port: {name}")
            return inport
    else:
        print(f"IN: Device '{target_name}' not found")
    #return midi_in_port

def init_midi_out():
    config = read_config('config.toml')
    ports = get_out_ports()
    target_name = config["MIDI"]['midi_output_port']
    for i, name in enumerate(ports):
        if target_name in name:
            outport = MidiOut()
            outport.open_port(i)
            print(f"OUT: Opened out port: {name}")
            return outport
    else:
        print(f"OUT: Device '{target_name}' not found")
    #return midi_in_port

def init_midi_aux_in():
    config = read_config('config.toml')
    ports = get_in_ports()
    target_name = config["MIDI"]['midi_aux_in_port']
    for i, name in enumerate(ports):
        if target_name in name:
            inport = MidiIn()
            inport.open_port(i)
            print(f"AUX: Opened aux in port: {name}")
            return inport
    else:
        print(f"AUX: Device '{target_name}' not found")
    #return midi_in_port



def read_config(file):
    with open(file, "rb") as f:
        return tomllib.load(f)
    
def write_config(file, config):
    with open(file, "wb") as f:
        tomli_w.dump(config, f)

def read_map(file):
    with open(file, "r") as f:
        return json.load(f)

def write_map(file, data):
    with open(file, 'w') as file:
        json.dump(data, file, indent=2)

def midi_to_abc(midi_note):
    """Convert a MIDI note number to ABC-like notation with octave numbers and # for sharps."""
    # Note names in an octave (all uppercase)
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    note_name = notes[midi_note % 12]
    octave = midi_note // 12 - 1  # MIDI 0 = C-1, MIDI 60 = C4

    return f"{note_name}{octave}"

def midi_list_to_abc(midi_notes):
    text = ""
    for note in midi_notes:
        text += midi_to_abc(note) + " "
    return text


def text_map():
    
    map = read_map("midi_map.json")
    text = "MIDI Mappings\nTrigger : Chord\n"
    for i in map["map"]:
        text += str(midi_to_abc(int(i))) + f" or {i}" + ": "
        for j in map["map"][i]:
            text += str(midi_to_abc(int(j))) + " "
        print(text)
        text = ""
    return text