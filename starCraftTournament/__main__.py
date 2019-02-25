# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2019 Christian Schwarz

from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer

# Terran vs. Protoss
# from custom_bots.terran import TerranBot
# run_game(maps.get("Abyssal Reef LE"), [
#     Bot(Race.Terran, TerranBot()),
#     Computer(Race.Protoss, Difficulty.Medium)
# ], realtime=False)

# Zerg vs. Protoss
from custom_bots.zerg import ZergBot
run_game(maps.get("Abyssal Reef LE"), [
    Bot(Race.Zerg, ZergBot()),
    Computer(Race.Protoss, Difficulty.Medium)
], realtime=True)

# Protoss vs. Protoss
# from custom_bots.protoss import ProtossBot
# run_game(maps.get("Abyssal Reef LE"), [
#    Bot(Race.Protoss, ProtossBot()),
#    Computer(Race.Protoss, Difficulty.Medium)
# ], realtime=False)
