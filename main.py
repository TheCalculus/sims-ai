import math
from random import *

class GLOBALS(object):
    def __init__(self):
        self._broadcasts = []
        self._observers = []
    
    @property
    def BROADCASTS(self):
        return self._broadcasts

    @BROADCASTS.setter
    def BROADCASTS(self, value):
        self._broadcasts.append(value)
        for callback in self._observers:
            callback(self._broadcasts)

    def bind_to(self, callback):
        self._observers.append(callback)

# the five basic personality traits by D. W. Fiske
class Traits():
    def __init__(self, extraversion, openness, agreeableness, conscientiousness, neuroticism):
        self.EXTRAVER = extraversion 
        self.OPENNESS = openness
        self.AGREEABL = agreeableness
        self.CONSCIEN = conscientiousness
        self.NEUROTIC = neuroticism

class Stats():
    def __init__(self, hunger, energy, hygiene, bladder, fun, social):
        self.HUNGER  = hunger
        self.ENERGY  = energy
        self.HYGIENE = hygiene
        self.BLADDER = bladder
        self.FUN     = fun
        self.SOCIAL  = social

class Object():
    def __init__(self, broadcasts, name, advertisements, utility):
        self.name = name
        self.advertisements = advertisements # personality
        self.utility = utility # stats
        self.proximity = 0
        self.broadcasts = broadcasts

    def broadcast(self):
        self.broadcasts.BROADCASTS = self

class Sim():
    def __init__(self, broadcasts, name, traits=None, stats=None):
        self.name   = name
        self.traits = traits if traits is not None else Traits(random(), random(), random(), random(), random())
        self.stats  = stats  if stats  is not None else Stats(1, 1, 1, 1, 1, 1)
        self.broadcasts = broadcasts
        self.broadcasts.bind_to(self.broadcast_listener)

    def broadcast_listener(self, broadcasts):
        # a new item broadcasted itself
        print(f"Object '{broadcasts[-1].name}' broadcasted")

    def print_dict(self, dict):
        for dict_item, dict_value in dict.__dict__.items():
            padding = 8 - len(dict_item)
            print(f"{dict_item}{padding * ' '} : {dict_value}")

    def print_char(self):
        print(f"{'-'*10} {self.name} {'-'*10}")
        self.print_dict(self.traits)
        self.print_dict(self.stats)
        print(f"{'-'*11}{'-'*len(self.name)}{'-'*11}")

if __name__ == '__main__':
    globals = GLOBALS()

    jacob = Sim(globals, "Jacob")
    jacob.print_char()

    fridge = Object(globals, "Fridge", {}, {
        "HUNGER":   10,
        "ENERGY":    5,
        "BLADDER": -10,
        "HYGIENE":  -5,
    })
    fridge.broadcast()
