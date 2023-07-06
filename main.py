import math
from random import *

# the five basic personality traits by D. W. Fiske
class Traits():
    def __init__(self, extraversion, openness, agreeableness, conscientiousness, neuroticism):
        self.EXTRAVER = extraversion 
        self.OPENNESS = openness
        self.AGREEABL = agreeableness
        self.CONSCIEN = conscientiousness
        self.NEUROTIC = neuroticism

class Sim:
    def __init__(self, name, traits = Traits(random(), random(), random(), random(), random())):
        self.name   = name
        self.traits = traits
        
    def print_traits(self):
        print(f"{self.name} traits:")
        for trait in self.traits.__dict__:
            trait_value = getattr(self.traits, trait)
            print(f"{trait}: {trait_value * 100 : 0.2f}% (other {trait_value})")

jacob = Sim("Jacob")
jacob.print_traits()
