# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2019 Christian Schwarz

import os
import random
import textwrap

from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer


def parse_arguments():
    """Parses the command line arguments.

    Returns:
        Args: Containing the parsed command line arguments.
    """
    import argparse
    parser = argparse.ArgumentParser(
        description=textwrap.dedent("""This script runs the Signavio database schema tests."""),
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("--bot",
                        dest="bot",
                        type=str,
                        help=textwrap.dedent("""\
                            Determines the bot that should be used.
                        """))

    parser.add_argument("--difficulty",
                        dest="difficulty",
                        help=textwrap.dedent("""\
                            Determines the difficulty of the AI which the bot plays against. This should be:
                                Easy, Medium, Hard, or VeryHard
                        """),
                        default=None)

    parser.add_argument("--enemy",
                        dest="enemy",
                        help=textwrap.dedent("""\
                            Determines the race of the enemy. This should be either Terran, Zerg, or Protoss.
                            The default is randomly chosen.
                        """),
                        default=None)

    parser.add_argument("--list-bots",
                        dest="list_bots",
                        help=textwrap.dedent("""\
                                Lists the available bots.
                            """),
                        action="store_true",
                        default=False)

    parser.add_argument("--realtime",
                        dest="realtime",
                        help=textwrap.dedent("""\
                                If this argument is present, the game will happen in realtime.
                            """),
                        action="store_true",
                        default=False)

    args = parser.parse_args()

    races = ("Terran", "Zerg", "Protoss")
    if args.enemy not in races:
        args.enemy = random.choice(races)

    difficulties = ("Easy", "Medium", "Hard", "VeryHard")
    if args.difficulty not in difficulties:
        args.difficulty = random.choice(difficulties)

    return args


def load_bots():
    """Loads and returns all bots.

    This is a manual operation for now.
    """
    from custom_bots.terran import TerranBot
    from custom_bots.zerg import ZergBot
    from custom_bots.protoss import ProtossBot

    bots = {
        "zerg": ZergBot,
        "terran": TerranBot,
        "protoss": ProtossBot
    }

    return bots


def play_against_ai(arguments, bots):
    """Let's the bot play against a predefined AI.

    Args:
        arguments (arguments): Command line given to starCraftTournament.
    """
    print(f"The bot will be playing against {arguments.enemy} (Difficulty: {arguments.difficulty}).")

    bot_class = bots[arguments.bot]

    run_game(maps.get("Abyssal Reef LE"), [
        Bot(getattr(Race, bot_class.race),
            bot_class()),
        Computer(getattr(Race, arguments.enemy),
                 getattr(Difficulty, arguments.difficulty))
    ], realtime=arguments.realtime)


def early_exit(arguments, bots):
    """Returns if an early exit, without a specific game is required.

    Args:
        arguments (arguments): Command line given to starCraftTournament.
        bots (dict): Dictionary of bots available for the starCraftTournament.

    Returns:
        bool: Returns True, in case the game should not be started, False otherwise.
    """
    if arguments.list_bots:
        print("The following bots are available:")
        for bot in bots:
            print(f"    * {bot} - {bots[bot].__doc__.split(os.linesep)[0].strip()}")

        return True

    if arguments.bot not in bots:
        print(f"{arguments.bot} is an unknown bot. Please use --list-bots to get the names of all known bots.")
        return True

    return False


def main():
    """Starts the StarCraftTournament."""
    bots = load_bots()
    arguments = parse_arguments()

    if early_exit(arguments, bots):
        return

    play_against_ai(arguments, bots)


if __name__ == "__main__":
    main()
