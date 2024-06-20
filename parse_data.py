#!/usr/bin/env python

# name    :  parse_data.py
# version :  0.0.1
# date    :  20240619
# author  :  Leam Hall
# desc    :  Remove markup and parse data.


input_file = "data/raw_data.txt"

markup = ["[hr]", "[i]", "[/i]", "[spoiler]", "[/spoiler]", "[b]", "[/b]", "."]


def scrub_line(line):
    for mark in markup:
        if mark in line:
            line = line.replace(mark, "")

    return line.strip()


if __name__ == "__main__":
    with open(input_file, "r") as in_f:
        for line in in_f.readlines():
            line = scrub_line(line)
            print(line)
