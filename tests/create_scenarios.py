# date: 2026-5-29
# script qui créer le fichier json des scénarios de test :
# - note on/off, timing, PC
# - tous les CC de 1 à 43 pour les valeurs min et max
#
# pour tester :
# $ python3 test_receive.py & python3 send.py

import json

par_num = [
    134, 135, 
    63, 64, 68, 66, 42, 43, 47, 45, 21, 22, 26, 24, 0, 1, 5, 3,
    70, 49, 28, 7,
    79, 78, 58, 57, 37, 36, 16, 15,   
    137, 138, 139, 142, 143, 
    81, 60, 39, 18, 
    72, 73, 74, 75, 71, 76, 
    ]

parameters_max = [
    99,99,99,99,99,99,99,99,99,99,99,3, 3, 7, 3, 7, 99,1, 31, 99,14,  
    99,99,99,99,99,99,99,99,99,99,99,3, 3, 7, 3, 7, 99,1, 31, 99,14,  
    99,99,99,99,99,99,99,99,99,99,99,3, 3, 7, 3, 7, 99,1, 31, 99,14,  
    99,99,99,99,99,99,99,99,99,99,99,3, 3, 7, 3, 7, 99,1, 31, 99,14,  
    99,99,99,99,99,99,99,99,99,99,99,3, 3, 7, 3, 7, 99,1, 31, 99,14,  
    99,99,99,99,99,99,99,99,99,99,99,3, 3, 7, 3, 7, 99,1, 31, 99,14,  
    99,99,99,99,99,99,99,99, # PITCH EG
    31, 7, 1,
    99,99,99,99,1, 5, # LFO
    7, 48, # TRANSPOSE
    127, 127, 127, 127, 127, 127, 127, 127, # VOICE NAME
    63 # OP ON/OFF
    ]
    
class Scenario:
    """
    Une simple classe pour structurer les données :
    - message de référence de ce qui est testé
    - le code envoyé au module
    - le code qui doit être reçu du Volca FM
    """
    def __init__(self, message, send, expected):
        self.message = message
        self.send = send
        self.expected = expected

    def tojson(self):
        """
        Fonction de formatage des données en json.
        """    
        return """
    {
        "message": "%s",
        "send": %s,
        "expected": %s
    }""" % (self.message, self.send, self.expected)
    

    def fromcc(cc, value):    
        """
        Fonction qui calcule le code MIDI à envoyer et à recevoir
        et retourne le snénario correspondant.
        """
        algos = [0, 13, 7, 6, 4, 21, 30, 31]
        if 43 < cc:
            return Scenario("hors cc", [176, cc, value], [])
        msb = cc2index(cc)[4]
        lsb = cc2index(cc)[5]
        val = cc2index(cc)[6] * value // 127
        if cc == 1:
            val = value // 16
            val = algos[val]
        elif msb == 0 and lsb % 21 == 5:
            return Scenario("CC" + str(cc) + " " + str(value),
                [176, cc, value],
                [176, 99, msb, 176, 98, lsb, 176, 6, val,
                 176, 99, msb, 176, 98, lsb + 1, 176, 6, val,
                 176, 99, msb, 176, 98, lsb - 3, 176, 6, 0])
        return Scenario("CC" + str(cc) + " " + str(value),
            [176, cc, value],
            [176, 99, msb, 176, 98, lsb, 176, 6, val])


def cc2index(cc):
    """
    Fonction qui retourne le tuple des données utiles en fonction 
    du numéro de CC.  
    """
    l = [2, 16, 4, 8, 5, 4, 6]
    rank = cc - 1 # rang du paramètre dans la page
    for page in range(7): # numéro de page
        if (rank < l[page]):
            break;
        rank = rank - l[page]
    num = par_num[cc - 1]
    max = parameters_max[num]
    return (cc, page, rank, num, num // 128, num % 128, max)

def report():
    """
    Fonction de reporting qui affiche le tableau des données :
    |cc|page|rank|num|MSB|LSB|MAX|
    """
    print(f'|cc|page|rank|num|MSB|LSB|MAX|')
    for cc in range(1, 44):
        res = cc2index(cc)
        if res[2] == 0:
            print(f'|----------------------------|')
        print(f'|{res[0]:2d}|{res[1]:4d}|{res[2]:4d}|{res[3]:3d}|\
{res[4]:3d}|{res[5]:3d}|{res[6]:3d}|')
    print(f'|----------------------------|')

def build_scenarios():
    """
    Le constructeur qui retourne la liste des scénarios.
    """
    scenarios = []
    scenarios.append(Scenario("note on", [144, 60, 100], [144, 60, 100]))
    scenarios.append(Scenario("note off", [128, 60, 0], [128, 60, 0]))
    scenarios.append(Scenario("clock", [248], [248]))
    scenarios.append(Scenario("start", [250], [250]))
    scenarios.append(Scenario("stop", [252], [252]))
    scenarios.append(Scenario("Program Change", [192, 2], []))
    for cc in range(1, 45):
        scenarios.append(Scenario.fromcc(cc, 0))
        scenarios.append(Scenario.fromcc(cc, 127))
    return scenarios

def export():
    """
    Fonction d'exportation des scénarios au format json.
    """
    s = ""
    for scenario in build_scenarios():
        s += scenario.tojson() + ","
    f = open("scenarios.json", "w")
    f.write("[" + s[:-1] + "\n]\n")
    f.close()
    
if __name__ == '__main__':
    report()
    export()


    
