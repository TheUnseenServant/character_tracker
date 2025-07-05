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

#data_file = "data/orc_army.csv"

def parse_args():
    """ Parse the arguments """
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--comment", default="", help="Comment")
    parser.add_argument(
        "-d", "--dice", default=1, type=int, help="Number of d6 per roll"
    )
    parser.add_argument("-f", "--file", default="", help="File to use")
    parser.add_argument(
        "-n", "--num", default=1, type=int, help="How many rolls to make"
    )
    parser.add_argument(
        "-t", "--target", default=5, type=int, help="Target number"
    )
    return parser.parse_args()

def roll_dice(num, target, dice=1):
    """ roll the number of dice """
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
    """ Return a string of the results """
    results = ""
    if len(comment):
        results += "\n{}\n".format(comment)
    results += "Successes:  {}\n".format(successes)
    results += "Rolls:  {}\n".format(sorted(rolls, reverse=True))
    return results


def run_file(data_file):
    """ Runs the commands with the given data_file """
    with open(data_file, "r", newline="") as in_f:
        reader = csv.DictReader(
            in_f,
            fieldnames = ["comment", "num", "hd", "target"],
            delimiter=":")
            
        for row in reader:
            row["num"] = int(row["num"]) * int(row["hd"])
            successes, rolls = roll_dice(row["num"], int(row["target"]))
            print(return_results(row["comment"], successes, rolls))


if __name__ == "__main__":

    args = parse_args()
    if args.file:
        try:
            run_file(args.file)
        except FileNotFoundError:
            print("Could not find {}, exiting.".format(args.file))
            sys.exit(1)
    else:
        successes, rolls = roll_dice(args.num, args.target, args.dice)
        print(return_results(args.comment, successes, rolls))



