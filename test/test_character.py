#!/usr/bin/env python

# name    :  test/test_character.py
# version :  0.0.1
# date    :  20240428
# author  :  Leam Hall
# desc    :  Tests of the character and character builder objects

import os.path
import tempfile
import unittest

import write_char as wc


class TestCharacter(unittest.TestCase):
    def setUp(self):
        char_1_data = {
            "key": "jiho",
            "name": "Jing Ji-ho",
            "career": "Fighter",
        }
        self.char_1 = wc.Character(char_1_data)

    def test_character(self):
        self.assertEqual(self.char_1.key, "jiho")
        self.assertEqual(self.char_1.name, "Jing Ji-ho")
        self.assertEqual(self.char_1.career, "Fighter")


class TestCharacterBuilder(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.data_file = os.path.join(self.test_dir.name, "data.csv")
        with open(self.data_file, "w") as f:
            f.write("key;name;career;xp;\n")
            f.write("jiho;Jing Ji-ho;Fighter;7186\n")
            f.write("siwoo;Jing Si-woo;Fighter;3709\n")

        ci = wc.CareerInfo(wc.career_data)

        self.characters = wc.CharacterBuilder.build(self.data_file, ci)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_characters_count(self):
        self.assertEqual(len(self.characters), 2)

    def test_characters_data(self):
        char_keys = self.characters.keys()
        self.assertIn("jiho", char_keys)

        jjh = self.characters["jiho"]
        self.assertEqual(type(jjh), wc.Character)
        self.assertEqual(jjh.key, "jiho")
        self.assertEqual(jjh.name, "Jing Ji-ho")
        self.assertEqual(jjh.career, "Fighter")
        self.assertEqual(jjh.xp, 7186)
