#!/usr/bin/env python

# name    :  parse_data.py
# version :  0.0.1
# date    :  20240619
# author  :  Leam Hall
# desc    :  Remove markup and parse data.

import re

input_file = "data/raw_data.txt"


def list_from_file(file):
    """Take a file, return the valid lines as a list"""
    data = []
    with open(file, "r") as f:
        for line in f:
            line = scrub_line(line)
            if line:
                data.append(line)
    return data


def scrub_line(line):
    """Remove markup."""
    line = re.sub("\\[\\/?[\\w]+\\]", "", line)
    line = " ".join(line.split())
    return line.strip()


if __name__ == "__main__":
    data = list_from_file(input_file)

    for line in data:
        print(line)
