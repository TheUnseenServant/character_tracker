#!/usr/bin/env python

# name    :  test/test_character.py
# version :  0.0.1
# date    :  20240428
# author  :  Leam Hall
# desc    :  Tests of the character and character builder objects

import os.path
import unittest

import write_char as wc

data = {
    "name": "Smiles",
    "title": "",
    "career": "Rogue",
    "level": 1,
    "hd": 1,
    "hp": 1,
    "sd": 0,
    "sp": 0,
    "alignment": "Lawful",
    "aac": "",
    "enc": "",
    "stats": ["int +1"],
    "feats": ["Ciphers"],
    "skills": ["Spy"],
    "weapons": ["Short sword", "Self bow"],
    "armor": ["Leather", "Shield"],
    "gear": ["Rogue's tools"],
    "silver": 5,
    "liege": "Gar",
    "morale": 0,
    "loyalty": 0,
}


class TestCharacter(unittest.TestCase):
    def setUp(self):
        char_1_data = {
            "key": "jiho",
            "name": "Jing Ji-ho",
            "career": "Fighter",
        }
        self.char_1 = wc.Character(char_1_data)
        self.char_2 = wc.Character(char_1_data)

    def test_character(self):
        self.assertEqual(self.char_1.key, "jiho")
        self.assertEqual(self.char_1.name, "Jing Ji-ho")
        self.assertEqual(self.char_1.career, "Fighter")

    def test_update_character(self):
        empty_data = {"level": 1, "hd": 1, "hp": 1, "sd": 0, "sp": 0}
        self.char_2 = wc.update_character(self.char_2, empty_data)
        self.assertTrue(hasattr(self.char_2, "level"))
        self.assertEqual(self.char_2.level, 1)
        self.assertTrue(hasattr(self.char_2, "sp"))
        self.assertEqual(self.char_2.sp, 0)


class TestRenderTemplate(unittest.TestCase):

    def setUp(self):
        self.character = wc.Character(data)

    def test_render_template_base(self):
        base_template = "${name} ${career}"
        expected = "Smiles Rogue"
        result = wc.render_template(base_template, self.character)
        self.assertEqual(expected, result)

    def test_render_template_bbcode(self):
        bbcode_template_file = os.path.join("templates", "bbcode.tmpl")
        if os.path.isfile(bbcode_template_file):
            with open(bbcode_template_file, "r") as in_f:
                bbcode_template = in_f.read()
        else:
            print("Cannot find {}".format(bbcode_template_file))
        result = wc.render_template(bbcode_template, self.character)
        self.assertIn("Smiles", result)
