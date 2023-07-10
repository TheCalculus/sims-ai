from math import exp
from random import random, randint, uniform
from time import sleep


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
            "ANGER": uniform(0.25, 1),
            "ACTIVE": uniform(0.25, 1),
            "CHEER": uniform(0.25, 1),
            "GENIUS": uniform(0.25, 1),
            "CREATIVE": uniform(0.25, 1),
            "LAZY": uniform(0.25, 1),
            # implement proximity measuring to object to show this
            "SOCIAL": uniform(0.25, 1),
        }
        stats = stats or {
            "HUNGER": random(),
            "ENERGY": random(),
            "HYGIENE": random(),
            "BLADDER": random(),
            "FUN": random(),
            "SOCIAL": random(),
            "SATISF": random(),  # increased to promote behaviors that reflect traits
        }
        self.name = name
        self.traits = traits
        self.stats = dict(stats)
        self.wants = {}
        self.broadcasts = broadcasts
        self.broadcasts.bind_to(self.broadcast_listener)

    def reduce_stats(self):
        for stat in self.stats:
            self.stats[stat] -= random() / 10
            if self.stats[stat] < 0:
                self.stats[stat] = 0
        if (
            self.stats["HUNGER"] < 0.15
            or self.stats["HYGIENE"] < 0.05
            or self.stats["BLADDER"] < 0.1
            or self.stats["ENERGY"] < 0.05
        ):
            print("sim failed to maintain itself")
            exit()

    def weigh_stats(self):
        wants = {}

        wants["HUNGER"] = (1 / exp(self.stats["HUNGER"])) ** 4
        wants["ENERGY"] = (1 / exp(self.stats["ENERGY"])) ** (
            7 - 7 * self.traits["ACTIVE"]
        )
        wants["HYGIENE"] = 1 - self.stats["HYGIENE"] ** (1 / 2)
        wants["BLADDER"] = 1 - self.stats["BLADDER"] ** (1 / 3)
        wants["FUN"] = 1 - self.stats["FUN"] ** self.traits["SOCIAL"]
        wants["SOCIAL"] = wants["FUN"]
        wants["SATISF"] = 1 / exp(self.stats["SATISF"])

        return sorted(wants.items(), key=lambda x: x[1], reverse=True)

    def broadcast_listener(self, broadcasts):
        # a new item broadcasted itself
        print(f"Object '{broadcasts[-1].name}' broadcasted")
        weighed_stats = self.weigh_stats()
        preference = weighed_stats[randint(0, 1)]
        print(f"Sim chose {preference[0]}...\n...with priorities {weighed_stats}")
        self.stats[preference[0]] += 0.5
        if self.stats[preference[0]] > 1:
            self.stats[preference[0]] = 1

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
        {  # TODO: weight these on the basis of needs.
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

    for i in range(10):
        jacob.reduce_stats()
        jacob.print_char()
        fridge.broadcast()
        sleep(1)
