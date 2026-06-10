# fichier : freq.py
# auteur : Pierrick MEIGNEN
# date : 2026-6-7
# licence : GNU GPL version 3

"""
Un script pour calculer les valeurs de FINE en fonction de COARSE pour obtenir
les 12 notes de la gamme.
"""
from math import *

notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def get_values(coarse):
    min = 12 * log(coarse) / log(2)
    min = ceil(min)
    max = min + 12
    l = list(range(12))
    for note in range(min, max):
        value = round(100 * (exp(note * log(2) / 12) / coarse - 1))
        if value in [99, 100]:
            value = 0
        l[note % 12] = value
    return {"coarse":coarse, "values":l}

def print_values(d):
    print(f'|{str(d["coarse"]):6s}', end="|")
    for val in d["values"]:
        print(f"{val:2d}", end = "|")
    print()

def print_lines():
    print("|------|" + "--|" * 12)

def print_notes():
    L = [.5]
    L.extend(range(1, 32))
    for coarse in L:
        print(f"{str(coarse):3s}", end = "|")
        for fine in range(100):
            n = 12 * log(coarse * (1 + 0.01 * fine)) / log(2)
            m = round(n)
            if abs(m - n) < 0.05:
                #print(f"{m % 12:2d}", end = "|")
                print(f"{notes[m % 12]:2s}", end = "|")
        print()

def report():
    """
    affiche les valeurs de coarse et fine pour la fréquence la plus proche 
    de la note 
    """
    print("|coarse|", end="")
    for note in notes:
        print(f"{note:2s}", end = "|")
    print()
    print_lines()

    L = [.5]
    L.extend(range(1, 32))
    for coarse in L:
        d = get_values(coarse)
        print_values(d)

if __name__ == '__main__':
    print_notes()

