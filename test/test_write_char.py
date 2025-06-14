#!/usr/bin/env python

# name    :  test/test_character.py
# version :  0.0.1
# date    :  20240428
# author  :  Leam Hall
# desc    :  Tests of the character and character builder objects

import unittest

import write_char as wc

data = {
    "name": "Smiles",
    "title": "",
    "career": "Rogue",
    "level":    1,
    "hd":       1,
    "hp":       1,
    "sd":       0,
    "sp":       0,
    "alignment": "Lawful",
    "aac":      "",
    "enc":      "",
    "stats":    ["int +1"],
    "feats":    ["Ciphers"],
    "skills":   ["Spy"],
    "weapons":  ["Short sword", "Self bow"],
    "armor":    ["Leather", "Shield"],
    "gear":     ["Rogue's tools"],
    "silver":   5,
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


"""
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
"""
