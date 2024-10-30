#!/usr/bin/env python

# name    :  parse_data.py
# version :  0.0.1
# date    :  20240619
# author  :  Leam Hall
# desc    :  Remove markup and parse data.


input_file = "data/raw_data.txt"

markup = ["[hr]", "[i]", "[/i]", "[spoiler]", "[/spoiler]", "[b]", "[/b]", "."]

def list_from_file(file):
    """ Take a file, return the valid lines as a list """
    data = []
    with open(file, 'r') as f:
       for line in f:
            line = scrub_line(line, markup)
            if line:
                data.append(line) 
    return data


def scrub_line(line, markup = markup):
    """ Remove specified markup. """
    for mark in markup:
        if mark.lower() in line.lower():
            line = line.replace(mark, "")

    return line.strip()


if __name__ == "__main__":
    data = list_from_file(imput_file, markup)
    
    for line in data:
        print(line)

