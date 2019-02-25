# Welcome to the StarCraftTournament base package

The StarCraftTournament repository contains the necessary
parts to build your AI for the StarCraft II Tournament.

## Preparation
* Install [StarCraft II]
* Download the [maps]
* Install the other requirements with `pip install -t requirements.txt`

## Tutorials
https://www.youtube.com/watch?v=v3LJ6VvpfgI

## Implement your Tournament Bots
For now, we are still in the planning phase.
In case you already want to start the implementation of your tournament bot you can implement a faction
specific bot in:
  * Terran: `starCraftTournament.custom_bots.terran.TerranBot`
  * Zerg: `starCraftTournament.custom_bots.zerg.ZergBot`
  * Protoss: `starCraftTournament.custom_bots.protoss.ProtossBot`

## Test your Bot
For now, we only implemented the Bot vs. AI mode.
To test your bots, please modify `starCraftTournament.__main__.py` for now.

[StarCraft II]: https://starcraft2.com/en-us/
[maps]: https://github.com/Blizzard/s2client-proto