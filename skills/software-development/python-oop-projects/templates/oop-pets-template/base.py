#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Base class — change 'Pet' to your domain (Car, Unit, Employee)
"""

class Pet:
    def __init__(self, name, age, weight, kind):
        self.name = name
        self.age = age
        self.weight = weight
        self.kind = kind
        self._hunger = 50
        self._energy = 80
        self._health = 100
        self.happiness = 70
        self.medical_records = []

    def eat(self, amount):
        if amount <= 0:
            return False
        self._hunger = max(0, self._hunger - amount * 0.8)
        self._energy = min(100, self._energy + amount * 0.1)
        print(f"{self.name} ate — hunger {int(self._hunger)} energy {int(self._energy)}")
        return True

    def walk(self, minutes):
        if minutes <= 0:
            return False
        self._energy = max(0, self._energy - minutes * 0.5)
        self._hunger = min(100, self._hunger + minutes * 0.3)
        self.happiness = min(100, self.happiness + minutes * 0.2)
        print(f"{self.name} walked — energy {int(self._energy)}")
        return True

    def status(self):
        print(f"\n{self.name} ({self.kind}) | age:{self.age} | weight:{self.weight}")
        print(f"  hunger:{int(self._hunger)} energy:{int(self._energy)} health:{int(self._health)} happiness:{int(self.happiness)}")

    def __repr__(self):
        return f"<{self.kind} {self.name}>"
