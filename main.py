import math
from random import random, randint


class GLOBALS:
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


class Object:
    def __init__(self, broadcasts, name, advertisements, utility):
        self.name = name
        self.advertisements = advertisements  # personality
        self.utility = utility  # stats
        self.proximity = 0
        self.broadcasts = broadcasts

    def broadcast(self):
        self.broadcasts.BROADCASTS = self


class Sim:
    def __init__(self, broadcasts, name, traits=None, stats=None):
        traits = traits or {
            "ANGER": random(),
            "ACTIVE": random(),
            "CHEER": random(),
            "GENIUS": random(),
            "CREATIVE": random(),
            "LAZY": random(),
            "SOCIAL": random(),
        }
        stats = stats or {
            "HUNGER": random(),
            "ENERGY": random(),
            "HYGIENE": random(),
            "BLADDER": random(),
            "FUN": random(),
            "SOCIAL": random(),
            "SATISF": random(),  # increased to promote behaviours that reflect traits
        }
        self.name = name
        self.traits = traits
        self.stats = dict(stats)
        self.wants = {}
        self.broadcasts = broadcasts
        self.broadcasts.bind_to(self.broadcast_listener)

    def weigh_stats(self):
        wants = {}
        wants["HUNGER"] = (1 / math.exp(self.stats["HUNGER"])) ** 4  # (\frac{1}{e^x})^4
        wants["ENERGY"] = (1 / math.exp(self.stats["ENERGY"])) ** 7  # (\frac{1}{e^x})^7
        wants["HYGIENE"] = 1 - self.stats["HYGIENE"] ** (
            1 / 2
        )  # 1 - x^{\frac{1}{2}} (or sqrt(x))
        wants["BLADDER"] = 1 - self.stats["BLADDER"] ** (
            1 / 3
        )  # 1 - x^{\frac{1}{3}} (or cube root)
        wants["FUN"] = 1 - self.stats["FUN"] ** self.traits["SOCIAL"]
        wants["SOCIAL"] = wants["FUN"]
        wants["SATISF"] = 1 / math.exp(self.stats["SATISF"])  # \frac{1}{e^x}
        return sorted(wants.items(), key=lambda x: x[1], reverse=True)

    def broadcast_listener(self, broadcasts):
        # a new item broadcasted itself
        print(f"Object '{broadcasts[-1].name}' broadcasted")
        weighed_stats = self.weigh_stats()
        preference = weighed_stats[randint(0, 2)]
        print(f"Sim chose {preference}...\n...with priorities {weighed_stats}")

    def print_dict(self, dictionary):
        for dict_item, dict_value in dictionary.items():
            padding = 8 - len(dict_item)
            print(f"{dict_item}{padding * ' '}: {dict_value}")

    def print_char(self):
        print(f"{'-' * 10} {self.name} {'-' * 10}")
        self.print_dict(self.traits)
        self.print_dict(self.stats)
        print(f"{'-' * 11}{'-' * len(self.name)}{'-' * 11}")


if __name__ == "__main__":
    globals_obj = GLOBALS()

    jacob = Sim(globals_obj, "Jacob")
    jacob.print_char()

    fridge = Object(
        globals_obj,
        "Fridge",
        {  # TODO: weight these on basis of needs.
            # a starving person should not lose "active" as much as a full person
            "ACTIVE": -3,
            "CHEER": 4,
            "LAZY": 6,
        },
        {
            "HUNGER": 10,
            "ENERGY": 5,
            "BLADDER": -10,
            "HYGIENE": -5,
        },
    )
    fridge.broadcast()
