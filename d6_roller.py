#!/usr/bin/env python

# name    :  d6_roller.py
# version :  0.0.1
# date    :  20250627
# author  :  Leam Hall
# desc    :  Rolls a certain number of d6 and checks for a target.


import argparse
import csv
import random
import sys


def parse_args(args):
    """Parse the arguments"""
    parser = argparse.ArgumentParser(
        description="Roll 'dice' d6 against a target, 'num' times",
        epilog=usage(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-c", "--comment", default="", help="Comment")
    parser.add_argument(
        "-d",
        "--dice",
        default=1,
        type=int,
        help="Number of d6 per roll (default 1)",
    )
    parser.add_argument("-f", "--file", default="", help="File to use")
    parser.add_argument(
        "-n",
        "--num",
        default=1,
        type=int,
        help="How many rolls to make (default 1)",
    )
    parser.add_argument(
        "-t",
        "--target",
        default=5,
        type=int,
        help="Target number (default 5) ",
    )
    result = parser.parse_args(args)
    result.file = result.file.strip()
    return result


def usage():
    """The extended usage help"""
    string = "For a 4 HD attack against a Target of 5:\n"
    string += "    ./d6_roller.py -n 4     # The default Target is 5\n\n"
    string += "For 3 attackers at 2 HD, multiply the attackers time the HD:\n"
    string += "    ./d6_roller.py -n 6\n\n"
    string += "For 3 saving throws (2d6) against an 8 save:\n"
    string += "    ./d6_roller.py -n 3 -d 2 -t 8\n\n"
    string += "If a file is given then it overrides the other arguments.\n"
    string += "The colon delimited file format is:\n"
    string += "    comment:num:dice:target\n\n"
    return string


def roll_dice(num, target, dice=1):
    """roll the number of dice"""
    successes = 0
    rolls = list()
    for x in range(num):
        roll = 0
        for y in range(dice):
            roll += random.randint(1, 6)
        rolls.append(roll)
        if roll >= target:
            successes += 1
    return successes, rolls


def return_results(comment, successes, rolls):
    """Return a string of the results"""
    results = ""
    if len(comment):
        results += "\n{}\n".format(comment)
    results += "Successes:  {}\n".format(successes)
    results += "Rolls:  {}\n".format(sorted(rolls, reverse=True))
    return results


def run_file(data_file):
    """Runs the commands with the given data_file"""
    with open(data_file, "r", newline="") as in_f:
        reader = csv.DictReader(
            in_f,
            fieldnames=["comment", "num", "dice", "target"],
            delimiter=":",
        )

        for row in reader:
            num = int(row["num"])
            target = int(row["target"])
            dice = int(row["dice"])
            comment = row["comment"]
            successes, rolls = roll_dice(num, target, dice)
            print(return_results(comment, successes, rolls))


if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    if args.file:
        try:
            run_file(args.file)
        except FileNotFoundError:
            print("Could not find {}, exiting.".format(args.file))
            sys.exit(1)
    else:
        successes, rolls = roll_dice(args.num, args.target, args.dice)
        print(return_results(args.comment, successes, rolls))
