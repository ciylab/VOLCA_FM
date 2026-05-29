# date: 2026-5-29
# script qui lit les sorties MIDI et les compare aux scénarios.

import json
import sys
import time

import rtmidi
import rtmidi.midiutil

INPUT_PORT = 1
OUTPUT_PORT = 1

midi_in = rtmidi.MidiIn()
midi_in.open_port(INPUT_PORT)
midi_in.ignore_types(timing=False)

def io_test():
    rtmidi.midiutil.list_input_ports()
    rtmidi.midiutil.list_output_ports()

"""
Cette fonction lit un paquet d'octets reçus dont la longueur
est celle du paquet attendu dans le json. Si le message lu est
le message attendu alors on continue sinon c'est un bug.
"""
def test(data):
    received = []
    while True:
        msg = midi_in.get_message()
        if msg:
            received += msg[0]
        if len(received) == len(data["expected"]):
            assert received == data["expected"], data["message"]
            break

if __name__ == '__main__':
    # io_test()
    f = open("scenarios.json", 'r')
    for data in json.load(f):
        test(data)
    f.close()
    midi_in.close_port()
    del midi_in
