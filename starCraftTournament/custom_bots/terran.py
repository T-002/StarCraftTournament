# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2019 Christian Schwarz

import sc2
from sc2.constants import COMMANDCENTER
from sc2.constants import SCV

class TerranBot(sc2.BotAI):
    """A bot that is able to play the Terran faction."""

    async def on_step(self, iteration):
        """This method gets executed during each step of the game.

        You can threat this as you execution loop for the bot.
        """
        await self.distribute_workers()
        await self.train_scv()

    async def train_scv(self):
        """Trains a SCV."""
        for command_center in self.units(COMMANDCENTER).ready.noqueue:
            if self.can_afford(SCV):
                await(self.do(command_center.train(SCV)))
