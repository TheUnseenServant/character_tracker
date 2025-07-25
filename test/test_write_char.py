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
    "key": "smiles",
    "name": "Smiles",
    "career": "Rogue",
    "level": 1,
    "hd": 1,
    "hp": 1,
    "sd": 0,
    "sp": 0,
    "xp": 0,
    "liege": "Gar",
    "morale": 0,
    "loyalty": 0,
    "alignment": "Lawful",
    "species": "half-orc",
    "gender": "female",
    "aac": "",
    "enc": "",
    "stats": ["int +1"],
    "feats": ["Ciphers"],
    "skills": ["Spy"],
    "weapons": ["Short sword", "Self bow"],
    "armor": ["Leather", "Shield"],
    "gear": ["Rogue's tools"],
    "silver": 5,
}


class TestCharacter(unittest.TestCase):
    def setUp(self):
        self.char_1 = wc.Character(data)
        self.char_2 = wc.Character(data)

    def test_character(self):
        self.assertEqual(self.char_1.key, "smiles")
        self.assertEqual(self.char_1.name, "Smiles")
        self.assertEqual(self.char_1.career, "Rogue")
        self.assertEqual(self.char_1.level, 1)
        self.assertEqual(self.char_1.hd, 1)
        self.assertEqual(self.char_1.hp, 1)
        self.assertEqual(self.char_1.sd, 0)
        self.assertEqual(self.char_1.sp, 0)
        self.assertEqual(self.char_1.xp, 0)
        self.assertEqual(self.char_1.liege, "Gar")
        self.assertEqual(self.char_1.morale, 0)
        self.assertEqual(self.char_1.loyalty, 0)
        self.assertEqual(self.char_1.alignment, "Lawful")
        self.assertEqual(self.char_1.species, "half-orc")
        self.assertEqual(self.char_1.gender, "female")
        self.assertEqual(self.char_1.aac, "")
        self.assertEqual(self.char_1.enc, "")
        self.assertEqual(self.char_1.stats, ["int +1"])
        self.assertEqual(self.char_1.feats, ["Ciphers"])
        self.assertEqual(self.char_1.skills, ["Spy"])
        self.assertEqual(self.char_1.weapons, ["Short sword", "Self bow"])
        self.assertEqual(self.char_1.armor, ["Leather", "Shield"])
        self.assertEqual(self.char_1.gear, ["Rogue's tools"])
        self.assertEqual(self.char_1.silver, 5)
        self.assertEqual(self.char_1.spells, [])
        self.assertEqual(self.char_1.npcs, [])
        self.assertEqual(self.char_1.notes, [])

    def test_update_character(self):
        pass
        empty_data = {"level": 4, "hd": 4, "hp": 1, "sd": 0, "sp": 0}
        self.char_2 = wc.update_character(self.char_2, empty_data)
        self.assertTrue(hasattr(self.char_2, "level"))
        self.assertEqual(self.char_2.level, 4)
        self.assertTrue(hasattr(self.char_2, "hd"))
        self.assertEqual(self.char_2.hd, 4)


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
