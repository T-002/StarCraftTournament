# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2019 Christian Schwarz

import sc2
from sc2.constants import NEXUS, PROBE

class ProtossBot(sc2.BotAI):
    """This class represents the base class for the tournament bots."""

    race = "Protoss"

    async def on_step(self, iteration):
        """This method gets executed during each step of the game.

        You can threat this as you execution loop for the bot.
        """
        await self.distribute_workers()
        await self.train_probe()

    async def train_probe(self):
        """Trains a Protoss Probe."""
        for nexus in self.units(NEXUS).ready.noqueue:
            if self.can_afford(PROBE):
                await(self.do(nexus.train(PROBE)))
