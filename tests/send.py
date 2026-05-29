# date: 2026-5-29
# script qui envoie le code MIDI des scénarios.

import json
import time
import rtmidi
import rtmidi.midiutil

INPUT_PORT = 1
OUTPUT_PORT = 1

def io_test():
    rtmidi.midiutil.list_input_ports()
    rtmidi.midiutil.list_output_ports()
    
if __name__ == '__main__':
    # io_test()
    midi_out = rtmidi.MidiOut()
    midi_out.open_port(OUTPUT_PORT)
    f = open("scenarios.json", 'r')
    for data in json.load(f):
        print("********** test : " + data["message"])
        midi_out.send_message(data["send"])
        time.sleep(5 / 1000)
    midi_out.close_port()
    del midi_out
    f.close()
    
