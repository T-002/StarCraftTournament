# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2019 Christian Schwarz
import sc2
from sc2.constants import HATCHERY, SPAWNINGPOOL, EXTRACTOR
from sc2.constants import LARVA, ZERGLING, QUEEN, OVERLORD, DRONE
from sc2.constants import AbilityId, EFFECT_INJECTLARVA
from sc2.constants import RESEARCH_ZERGLINGMETABOLICBOOST

import random

class ZergBot(sc2.BotAI):
    """A bot that is able to play the Zerg faction."""

    rush_start_count = 24
    rush_break_count = 8

    drone_count = 16
    overlord_train_threshold = 3


    def __init__(self):
        """Initializes the ZergBot."""
        self.attack = False

        self.started_vespene_collection = False
        self.stopped_vespene_collection = False

        self.vespene_drones = []

        self.metabolic_boost_started = False
        self.queen_started = False

    async def infect_larvae(self):
        """Infects a hatchery with additional larvae."""
        for queen in self.units(QUEEN).idle:
            abilities = await self.get_available_abilities(queen)
            if AbilityId.EFFECT_INJECTLARVA in abilities:
                await self.do(queen(EFFECT_INJECTLARVA, self.units(HATCHERY).closest_to(queen)))

    async def train_units(self):
        """Trains all required units."""
        larvae = self.units(LARVA)
        if not larvae.exists:
            return

        if self.supply_left < self.overlord_train_threshold and \
                self.already_pending(OVERLORD) < self.units(HATCHERY).amount:
            if self.can_afford(OVERLORD):
                await self.do(larvae.random.train(OVERLORD))

        if self.units(DRONE).amount + self.already_pending(DRONE) < self.drone_count:
            if self.can_afford(DRONE):
                await self.do(larvae.random.train(DRONE))

        if self.units(SPAWNINGPOOL).ready.exists:
            for larva in larvae:
                if self.can_afford(ZERGLING):
                    await self.do(larva.train(ZERGLING))

        if self.units(SPAWNINGPOOL).ready.exists and not self.queen_started:
            for hatchery in self.units(HATCHERY):
                queens = self.units(QUEEN).closer_than(6, hatchery.position)
                if not queens.exists:
                    if self.can_afford(QUEEN) and hatchery.noqueue:
                        await self.do(hatchery.train(QUEEN))

    async def rush_with_zerglings(self):
        """Rushes the enemy in case all requirements are meet."""
        target = self.known_enemy_structures.random_or(self.enemy_start_locations[0]).position

        zerglings = self.units(ZERGLING)
        if zerglings.exists and (zerglings.amount > self.rush_start_count or self.attack):
            self.attack = True
            for zergling in zerglings:
                await self.do(zergling.attack(target))

    async def scout(self):
        """Scouts the map using OVERLORDS."""
        for overlord in self.units(OVERLORD).idle:
            expansion_locations = self.expansion_locations
            enemy_start_positions = self.enemy_start_locations
            scout_locations = [location for location in expansion_locations if location not in enemy_start_positions]
            await self.do(overlord.move(random.choice(scout_locations)))

    async def build_extractor(self):
        """Builds one EXTRACTOR."""
        if self.units(EXTRACTOR).exists:
            return

        if self.already_pending(EXTRACTOR):
            return

        if self.can_afford(EXTRACTOR) and self.workers.exists:
            drone = self.workers.random
            target = self.state.vespene_geyser.closest_to(drone.position)
            await self.do(drone.build(EXTRACTOR, target))

    async def build_spawningpool(self):
        """Builds the SPAWNINGPOOL."""
        if self.units(SPAWNINGPOOL).exists or self.already_pending(SPAWNINGPOOL):
            return

        if not self.workers.exists:
            return

        for d in range(4, 15):
            pos = self.units(HATCHERY).first.position.to2.towards(self.game_info.map_center, d)
            if await self.can_place(SPAWNINGPOOL, pos):
                drone = self.workers.closest_to(pos)
                if self.can_afford(SPAWNINGPOOL):
                    await self.do(drone.build(SPAWNINGPOOL, pos))

    async def manage_vespene_collection(self):
        """Manages the collection of Vespene."""
        if not self.units(EXTRACTOR).ready.exists:
            return

        if not self.started_vespene_collection:
            self.started_vespene_collection = True
            extractor = self.units(EXTRACTOR).first
            for drone in self.workers.random_group_of(2):
                self.vespene_drones.append(drone)
                await self.do(drone.gather(extractor))

            return

        if (self.vespene >= 100 or self.metabolic_boost_started) and self.vespene_drones:
            self.stopped_vespene_collection = True
            remaining_vespene_drones = []

            for drone in self.vespene_drones:
                mineral_fields = self.state.mineral_field.closer_than(10, drone.position)
                error = await self.do(drone.gather(mineral_fields.random, queue=True))
                if error:
                    remaining_vespene_drones.append(drone)

            self.vespene_drones = remaining_vespene_drones

    async def research(self):
        """Researches unit abilities."""
        if self.metabolic_boost_started:
            return

        pool = self.units(SPAWNINGPOOL).ready
        if not pool.exists:
            return

        if self.can_afford(RESEARCH_ZERGLINGMETABOLICBOOST):
            await self.do(pool.first(RESEARCH_ZERGLINGMETABOLICBOOST))
            self.metabolic_boost_started = True

    async def build_new_hatchery(self):
        """Builds a new hatchery."""
        if self.minerals < 500:
            return

        if not self.units(SPAWNINGPOOL).exists:
            return

        for d in range(4, 15):
            pos = self.units(HATCHERY).first.position.to2.towards(self.game_info.map_center, d)
            if await self.can_place(HATCHERY, pos):
                await self.do(self.workers.random.build(HATCHERY, pos))

    async def on_step(self, iteration):
        """The bots main loop.

        Args:
            iteration (int): Current iteration of the game.
        """
        if not self.units(HATCHERY).ready.exists:
            for unit in self.workers | self.units(ZERGLING) | self.units(QUEEN):
                await self.do(unit.attack(self.enemy_start_locations[0]))
            return

        await self.infect_larvae()
        await self.train_units()
        await self.scout()
        await self.rush_with_zerglings()

        await self.build_extractor()
        await self.build_spawningpool()
        await self.build_new_hatchery()
        await self.research()

        await self.manage_vespene_collection()
