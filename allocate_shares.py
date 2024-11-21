#!/usr/bin/env python

# name    :  allocate_shares.py
# version :  0.0.1
# date    :  20231010
# author  :  Leam Hall
# desc    :  Dividing up shares


# TODO
#   CSV file or similar for party data.
#   CLI options for coin, xp

import argparse
import csv

import sys


class Group:
    def __init__(self, data):
        self.key = data.get("key", "")
        self.hp = int(data.get("hp", 0))
        self.count = int(data.get("count", 0))


class Member:
    def __init__(self, data={}):
        self.name = data.get("name", "")
        self.coin_shares = float(data.get("coin_shares", 0.0))
        self.xp_shares = float(data.get("xp_shares", 0))
        self.mis_shares = self.coin_shares

    def give_shares(self, share):
        """Assigns coin and XP based on one share times share rate."""
        self.mis = int(share.mis * self.mis_shares)
        self.coins = int(share.coin * self.coin_shares)
        self.xps = int(share.xp * self.xp_shares)

    def __str__(self):
        return "{} gets {} XP and {} coin.".format(
            self.name,
            self.xps,  # The coin xps are added in Treasure.run_changes()
            self.coins + self.mis,
        )


class Monster:
    def __init__(self, data={}):
        self.key = data.get("key", "")
        self.name = data.get("name", "")
        self.base_xp = int(data.get("base_xp", 0))
        self.hp_xp = int(data.get("hp_xp", 0))

    def __str__(self):
        return "{} ({}) Base {} + {} per HP".format(
            self.name, self.key, self.base_xp, self.hp_xp
        )


class Treasure:
    def __init__(self, data={}):
        self.coin = data.get("coin", 0)
        self.coin_xp = self.coin
        self.xp = data.get("xp", 0)
        self.mis = data.get("mis", 0)
        self.tax_rate = data.get("tax_rate", 0.0)
        self.run_changes()

    def run_changes(self):
        self.xp += self.coin_xp
        self.tax = self.coin * (self.tax_rate / 100)
        self.coin -= self.tax


class Shares:
    def __init__(self, data={}):
        self.coin_shares = data.get("coin_shares", 0)
        self.xp_shares = data.get("xp_shares", 0)
        self.mis_shares = self.coin_shares

    def one_share(self, treasure):
        """Returns how much a share of coin and XP is."""
        self.coin = 0
        self.xp = 0
        self.mis = 0
        if treasure.coin > 0:
            self.coin = treasure.coin // self.coin_shares
        if treasure.xp > 0:
            self.xp = treasure.xp // self.xp_shares
        if treasure.mis > 0:
            self.mis = treasure.mis // self.mis_shares

    def __str__(self):
        return "{} coin  {} xp  {} mis shares".format(
            self.coin_shares, self.xp_shares, self.mis_shares
        )


def usage():
    """Extended help message."""
    string = """
    Note that the files are semi-colon delimted. They are plain text
      and you can edit them as you see fit. You own any errors...


    allocate_shares.py looks for adventurers with the -f opion
        -f data/watchfort2.csv    # as an example

        The format is:
        key;name;career;xp;coin_shares;xp_shares
        'career' and 'xp' are not currently used.

    data/monster_manual.csv has the monster data in the format:
      key;name;base_xp;hp_xp

      The key is the same in the monsters file, and the math is such
        that total XP is base_xp + (hp_xp * hp)

    data/watchfort_monsters.csv has a list of monsters encountered:
      key;hp;count

      The key here is as above, and the hp is how many HP each of
        those monster types had. The count is how many of them there
        were. You can duplicate monsters of the same type or add them
        all up.

    """
    return string


def members_from_csv(filename):
    """Returns a list of members from a csv file."""
    members = []

    try:
        with open(filename, "r", newline="") as f:
            reader = csv.DictReader(f, delimiter=";")
            for line in reader:
                members.append(Member(line))
    except FileNotFoundError:
        raise
    else:
        return members


def something_from_csv(filename, klass, return_object=dict()):
    """Returns a dict of objects from a csv file."""

    something = return_object

    try:
        with open(filename, "r", newline="") as f:
            reader = csv.DictReader(f, delimiter=";")
            for line in reader:
                if isinstance(something, list):
                    something.append(klass(line))
                else:
                    something[line["key"]] = klass(line)
    except FileNotFoundError:
        raise
    else:
        return something


def xp_for_monsters(data, monsters):
    """Calculates XP based on monster type, HP, and count."""
    monster = monsters.get(data.key, False)
    if monster:
        return (monster.base_xp + (monster.hp_xp * data.hp)) * data.count
    else:
        return 0


def get_total_xp(groups, monsters):
    """Interate over the groups and totals the xp."""
    total_xp = 0
    for group in groups:
        total_xp += xp_for_monsters(group, monsters)

    return total_xp


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        epilog=usage(), formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-c", "--coin", default=0, help="Cash intake in unified coin", type=int
    )
    parser.add_argument("-x", "--xp", default=0, help="Bonus XP", type=int)
    parser.add_argument(
        "-m", "--mis", default=0, help="Magic Item Sales", type=int
    )
    parser.add_argument(
        "--monster_groups",
        default="data/monster_groups.csv",
        help="Monster Groups file",
    )
    parser.add_argument(
        "--monster_manual",
        default="data/monster_manual.csv",
        help="Monster Manual file",
    )
    parser.add_argument(
        "-f", "--file", default="adventure_party.csv", help="Intake file"
    )
    parser.add_argument(
        "-t", "--tax_rate", default=0.0, type=float, help="Percent Tax Rate"
    )
    args = parser.parse_args()

    try:
        party = something_from_csv(args.file, Member, dict())
        monster_manual = something_from_csv(
            args.monster_manual, Monster, dict()
        )
        monsters = something_from_csv(args.monster_groups, Group, list())
    except Exception as e:
        print("Exception:  ", e)
        sys.exit(1)

    base_xp = get_total_xp(monsters, monster_manual)

    treasure = Treasure(
        {
            "coin": args.coin,
            "xp": args.xp,
            "mis": args.mis,
            "tax_rate": args.tax_rate,
        }
    )

    treasure.xp += base_xp

    total_shares = {"coin_shares": 0.0, "xp_shares": 0.0}
    for m in party.values():
        total_shares["coin_shares"] += m.coin_shares
        total_shares["xp_shares"] += m.xp_shares

    shares = Shares(total_shares)

    print("Totals: ")
    print("  {:.2f} tax".format(treasure.tax))
    print("  {} coin after taxes".format(treasure.coin))
    print("  {} base XP".format(base_xp))
    print("  {} base XP + (pre-tax) coin XP".format(treasure.xp))
    print("  {} total coin".format(treasure.coin + treasure.mis))
    print("")

    print(
        "There are {} coin and {} xp shares.\n".format(
            total_shares["coin_shares"], total_shares["xp_shares"]
        )
    )
    shares.one_share(treasure)

    for m in party.values():
        m.give_shares(shares)
        print(m)

    usage()
