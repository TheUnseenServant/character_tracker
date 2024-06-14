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
        return "{} gets {} coin and {} XP. he has {} coin shares".format(
            self.name,
            self.coins + self.mis,
            self.xps + self.coins,
            self.coin_shares,
        )


class Treasure:
    def __init__(self, data={}):
        self.coin = data.get("coin", 0)
        self.coin_xp = self.coin
        self.xp = data.get("xp", 0)
        self.mis = data.get("mis", 0)
        self.tax_rate = data.get("tax_rate", 0.05)
        self.run_changes()

    def run_changes(self):
        self.xp += self.coin_xp
        self.tax = self.coin * self.tax_rate
        self.coin -= self.tax


class Shares:
    def __init__(self, data={}):
        self.coin_shares = data.get("coin_shares", 0)
        self.xp_shares = data.get("xp_shares", 0)
        self.mis_shares = self.coin_shares

    def one_share(self, treasure):
        """Returns how much a share of coin and XP is."""
        print("treasure.coin is ", treasure.coin)
        print("coin_shares is  ", self.coin_shares)

        self.coin = treasure.coin // self.coin_shares
        self.xp = treasure.xp // self.xp_shares
        self.mis = treasure.mis // self.mis_shares

    def __str__(self):
        return "{} coin  {} xp  {} mis shares".format(
            self.coin_shares, self.xp_shares, self.mis_shares
        )


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


def one_share(total_shares, treasure):
    """Returns how much a share of coin and XP is."""
    coin = treasure.coin // total_shares["coin"]
    xp = treasure.xp // total_shares["xp"]
    results = {
        "coin": int(coin),
        "xp": int(xp),
    }
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--coin", default=0, help="Cash intake in unified coin", type=int
    )
    parser.add_argument("-x", "--xp", default=0, help="XP intake", type=int)
    parser.add_argument(
        "-m", "--mis", default=0, help="Magic Item Sales", type=int
    )
    parser.add_argument(
        "-f", "--file", default="data/adventure_party.csv", help="Intake file"
    )
    args = parser.parse_args()

    treasure = Treasure(
        {
            "coin": args.coin,
            "xp": args.xp,
            "mis": args.mis,
        }
    )

    try:
        party = members_from_csv(args.file)
    except Exception:
        print("Could not read file:  ", e)
        sys.exit(1)

    total_shares = {"coin_shares": 0.0, "xp_shares": 0.0}
    for m in party:
        print(m)

        total_shares["coin_shares"] += m.coin_shares
        total_shares["xp_shares"] += m.xp_shares

    print("Totals: ")
    print("  {:.2f} tax".format(treasure.tax))
    print("  {} coin after taxes".format(treasure.coin))
    print("  {} base + (pre-tax) coin XP".format(treasure.xp))
    print("  {} total coin".format(treasure.coin + treasure.mis))
    print("")

    print(
        "There are {} coin and {} xp shares.\n".format(
            total_shares["coin_shares"], total_shares["xp_shares"]
        )
    )
    shares = Shares(total_shares)
    print(str(shares))
    print(treasure)

    shares.one_share(treasure)

    for m in party:
        m.give_shares(shares)
        print(m)
