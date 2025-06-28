#!/usr/bin/env python

# name    :  d6_roller.py
# version :  0.0.1
# date    :  20250627
# author  :  Leam Hall
# desc    :  Rolls a certain number of d6 and checks for a target.


import argparse
import random


parser = argparse.ArgumentParser() 
parser.add_argument(
    "-n", "--num", 
    default=1, 
    type = int,
    help="How many rolls to make")
parser.add_argument(
    "-t", "--target", 
    default=5, 
    type = int,
    help="Target number")
parser.add_argument(
    "-d", "--dice", 
    default=1, 
    type = int,
    help= "Number of d6 per roll")
args = parser.parse_args()

successes = 0
rolls = list()
for x in range(args.num):
    roll = 0
    for y in range(args.dice):
        roll += random.randint(1,6)
    rolls.append(roll)
    if roll >= args.target:
        successes += 1


print("Successes:  ", successes)
print("Rolls (reverse order):  ", sorted(rolls, reverse=True))



