#!/usr/bin/env python

# name    :  get_keys.py
# version :  0.0.1
# date    :  20250704
# author  :
# desc    :

from os import listdir
from os.path import isfile, join

filepath = "/usr/local/src/theunseenservant/character_tracker/characters/base"
filelist = [f for f in listdir(filepath) if isfile(join(filepath, f))]

print(filelist)
keys = list()

for file in filelist:
    full_file_name = join(filepath, file)
    with open(full_file_name, "r") as in_f:
        for line in in_f:
            if ":" in line:
                key = line.split(":")[0].strip()
                keys.append(key)

keyset = set(sorted(keys))
print(keyset)
