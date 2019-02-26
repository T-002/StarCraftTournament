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
In case you already want to start the implementation of your tournament
bot you can implement a faction specific bot in:
  * Terran: `starCraftTournament.custom_bots.terran.TerranBot`
  * Zerg: `starCraftTournament.custom_bots.zerg.ZergBot`
  * Protoss: `starCraftTournament.custom_bots.protoss.ProtossBot`

## Test your Bot
For now, we only implemented the Bot vs. AI mode.

To get a detailed view of all supported options, please use
```
    python starCraftTournament --help
```

In general, the following commands are supported

  * *--bot*: Determines the bot to be started.
      The bots are defined in a dictionary in `starCraftTournament/__main__.py:load_bots()`.
  * *--difficulty*: Determines the difficulty of the AI which 
      the bot plays against. This should be
      `Easy`, `Medium`, `Hard`, or `VeryHard`.
      The default is randomly chosen from the available options.
  * *--enemy*: Determines the race of the enemy.
      This should be either `Terran`, `Zerg`, or `Protoss`.
      The default is randomly chosen from the available options.
  * *--list-bots*: Prints a list with all available bots.
  * *--realtime*: If this is present, the game will happen in realtime. If not, it runs as fast as possible.
 

As an example, the command

```
    python starCraftTournament --bot=zerg --enemy=Terran --difficulty=VeryHard
```
will start a game, using the bot `zerg` to compete against a very hard Terran AI at maximum speed.





[StarCraft II]: https://starcraft2.com/en-us/
[maps]: https://github.com/Blizzard/s2client-proto